import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestNormalReplacements(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('normal replacements')
    @allure.description('Verify normal replacements text info from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_normal_replacements_text_info(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that('PRIVACY_BODY_TEXT' in normal_replacements)
        assert_that('PRIVACY_CLOSE_TEXT' in normal_replacements)
        assert_that('APP_DESCRIPTION' in normal_replacements)
        assert_that('APP_NAME' in normal_replacements)
        assert_that('PRIVACY_CONTINUE_TEXT' in normal_replacements)
        assert_that('INCENTIVIZED_TITLE_TEXT' in normal_replacements)
        assert_that('INCENTIVIZED_BODY_TEXT' in normal_replacements)
        assert_that('INCENTIVIZED_CLOSE_TEXT' in normal_replacements)
        assert_that('INCENTIVIZED_CONTINUE_TEXT' in normal_replacements)
        assert_that('VUNGLE_PRIVACY_URL' in normal_replacements)

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('normal replacements')
    @allure.description('Verify normal replacements config from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_normal_replacements_config(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that('START_MUTED' in normal_replacements)
        assert_that('VIDEO_PROGRESS_BAR' in normal_replacements)
        assert_that('AUTO_LOCALIZE' in normal_replacements)
        assert_that('ACTION_TRACKING' in normal_replacements)

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('normal replacements')
    @allure.description('Verify normal replacements close button config from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_normal_replacements_close_button_config(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that('CTA_BUTTON_BACKGROUND' in normal_replacements)
        assert_that('CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements)
        assert_that('CTA_BUTTON_TEXT' in normal_replacements)
        assert_that('INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements)
        assert_that('FULL_CTA' in normal_replacements)
        assert_that('CTA_BUTTON_URL' in normal_replacements)

    @allure.feature('template settings')
    @allure.tag('normal', 'test_mode', 'PBJ20S1')
    @allure.story('fullscreen clickable')
    @allure.description('Test for fullscreen clickable - app flag false, placement no flag, mraid adm true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [full_screen_clickable_app_f])
    def test_app_f_placement_no(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, full_screen_clickable_app_f_placement_n,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        template_settings = ad_markup['templateSettings']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(template_settings['normal_replacements']['FULL_CTA'], False)

    @allure.feature('template settings')
    @allure.tag('normal', 'test_mode', 'PBJ20S1')
    @allure.story('fullscreen clickable')
    @allure.description('Test for fullscreen clickable - app flag false, placement flag true, mraid adm true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [full_screen_clickable_app_f])
    def test_app_f_placement_t_adm_mraid_t(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, full_screen_clickable_app_f_placement_t_mraid,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        template_settings = ad_markup['templateSettings']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(template_settings['normal_replacements']['FULL_CTA'], True)

    @allure.feature('template settings')
    @allure.tag('normal', 'test_mode', 'PBJ20S1')
    @allure.story('fullscreen clickable')
    @allure.description('Test for fullscreen clickable - app flag true, placement no flag, mraid adm true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [full_screen_clickable_app_t])
    def test_app_t_placement_no(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, full_screen_clickable_app_t_placement_n,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        template_settings = ad_markup['templateSettings']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(template_settings['normal_replacements']['FULL_CTA'], True)

    @allure.feature('template settings')
    @allure.tag('normal', 'test_mode', 'PBJ20S1')
    @allure.story('fullscreen clickable')
    @allure.description('Test for fullscreen clickable - app flag true, placement flag false, mraid adm true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [full_screen_clickable_app_t])
    def test_app_t_placement_f_adm_mraid_t(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, full_screen_clickable_app_t_placement_f_mraid,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        template_settings = ad_markup['templateSettings']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(template_settings['normal_replacements']['FULL_CTA'], False)

    # ------------------------------------------- close button delay --------------------------------------------------

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded single page, placement level control, app not skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_single_app_not_skippable_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "forceViewIncentivized": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level data:
        "is_skippable": true,
        "multiVideoCloseButtonDelay": 25,
        "multiECCloseButtonDelay": 26,
        "singleCloseButtonDelay": 27
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('27'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded single page, placement level control, app skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_rewarded_single_app_skippable_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "forceViewIncentivized": false,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level data:
        "is_skippable": true,
        "multiVideoCloseButtonDelay": 25,
        "multiECCloseButtonDelay": 26,
        "singleCloseButtonDelay": 27
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSP0', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('27'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded multi page with end card, placement level control, app not skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_multi_app_not_skippable_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "forceViewIncentivized": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level data:
        "is_skippable": true,
        "multiVideoCloseButtonDelay": 25,
        "multiECCloseButtonDelay": 26,
        "singleCloseButtonDelay": 27
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RMP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('25'))
        assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('26'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded multi page with end card, placement level control, app skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_rewarded_multi_app_skippable_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "forceViewIncentivized": false,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level data:
        "is_skippable": true,
        "multiVideoCloseButtonDelay": 25,
        "multiECCloseButtonDelay": 26,
        "singleCloseButtonDelay": 27
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RMP0', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('25'))
        assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('26'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded single page, app level control, placement no setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_single_app_ctl(self, pub_app_id):
        '''
        Placement level data:
        "is_skippable": true

        App level data:
        "forceViewIncentivized": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded single page, app level control, placement setting null')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_single_app_ctl_1(self, pub_app_id):
        '''
        Placement level data:
        "is_skippable": true,
        "multi_video_close_button_delay": null,
        "multi_ec_close_button_delay": null,
        "single_close_button_delay": null

        App level data:
        "forceViewIncentivized": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSA1', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'PBJ20S1', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded multi page with end card, app level control, placement level no setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_multi_app_ctl(self, pub_app_id):
        '''
        Placement level data:
        "is_skippable": true

        App level data:
        "forceViewIncentivized": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RMA', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('18'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded multi page with end card, app level control, placement level setting null')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_multi_app_ctl_1(self, pub_app_id):
        '''
        Placement level data:
        "is_skippable": true,
        "multi_video_close_button_delay": null,
        "multi_ec_close_button_delay": null,
        "single_close_button_delay": null


        App level data:
        "forceViewIncentivized": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RMA1', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('18'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial single page, placement level control, app skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_inter_single_app_skippable_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "forceView": false,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level data:
        "is_skippable": true,
        "multiVideoCloseButtonDelay" : 1,
        "multiECCloseButtonDelay" : 2,
        "singleCloseButtonDelay" : 3
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916ISP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('3'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial single page, placement level control, app not skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_inter_single_app_not_skippable_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "forceView": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level data:
        "is_skippable": true,
        "multiVideoCloseButtonDelay" : 1,
        "multiECCloseButtonDelay" : 2,
        "singleCloseButtonDelay" : 3
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916ISP0', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('3'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial multi page with end card, placement level control, app skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_inter_multi_app_skippable_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "forceView": false,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level data:
        "is_skippable": true,
        "multiVideoCloseButtonDelay" : 1,
        "multiECCloseButtonDelay" : 2,
        "singleCloseButtonDelay" : 3
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916IMP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('1'))
        assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('2'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial multi page with end card, placement level control, app not skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_inter_multi_app_not_skippable_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "forceView": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level data:
        "is_skippable": true,
        "multiVideoCloseButtonDelay" : 1,
        "multiECCloseButtonDelay" : 2,
        "singleCloseButtonDelay" : 3
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916IMP0', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('1'))
        assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('2'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial single page, app level control, app skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_inter_single_app_skippable_app_ctl(self, pub_app_id):
        '''
        App level data:
        "forceView": false,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level data:
        "is_skippable": true
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916ISA', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('12'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial single page, app level control, app not skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_inter_single_app_not_skippable_app_ctl(self, pub_app_id):
        '''
        App level data
        "forceView": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19

        Placement level data:
        "is_skippable": true
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916ISA0', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial multi page with end card, app level control, app skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_inter_multi_app_skippable_app_ctl(self, pub_app_id):
        '''
        App level data:
        "forceView": false,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level data:
        "is_skippable": true

        "multi_ec_close_button_delay":16
        "multi_video_close_button_delay":15
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916IMA', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('15'))
        assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('16'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial multi page with end card, app level control, app not skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_inter_multi_app_not_skippable_app_ctl(self, pub_app_id):
        '''
        App level data:
        "forceView": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level data:
        "is_skippable": true
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916IMA0', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('11'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded skip after has the higher prior than close button control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_skip_after_prior(self, pub_app_id):
        '''
        Placement level: skip_after=16
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50911', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('16'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial skip after has the higher prior than close button control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_inter_skip_after_prior(self, pub_app_id):
        '''
        Placement level: skip_after=16
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50910', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('16'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded app and placement not skippable, placement has setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_app_and_placement_not_skippable(self, pub_app_id):
        '''
        Kraken passes the INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS value as '9999' from ADM
        Kraken passes the EC_CLOSE_BUTTON_DELAY_SECONDS value as '6' for multi page from ADM

        App level data:
        "forceViewIncentivized": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level setting：
        "is_skippable": false,
        "multi_video_close_button_delay": 25,
        "multi_ec_close_button_delay": 26,
        "single_close_button_delay": 27
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50908', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        if 'EC_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements:
            assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('26'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded placement not skippable, placement has setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_rewarded_app_skippable_placement_not_skippable(self, pub_app_id):
        '''
        Kraken passes the INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS value as '9999' from ADM
        Kraken passes the EC_CLOSE_BUTTON_DELAY_SECONDS value as '6' for multi page from ADM

        App level data:
        "forceViewIncentivized": false,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level setting：
        "is_skippable": false,
        "multi_video_close_button_delay": 25,
        "multi_ec_close_button_delay": 26,
        "single_close_button_delay": 27
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM509080', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        if 'EC_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements:
            assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('26'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded app and placment not skippable, placement no setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_app_and_placement_not_skippable_1(self, pub_app_id):
        '''
        Kraken passes the INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS value as '9999' from ADM
        Kraken passes the EC_CLOSE_BUTTON_DELAY_SECONDS value as '6' for multi page from ADM

        App level data:
        "forceViewIncentivized": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level setting：
        "is_skippable": false
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM509081', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        if 'EC_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements:
            assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('18'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded placement not skippable, placement no setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_rewarded_app_skippable_placement_not_skippable_1(self, pub_app_id):
        '''
        Kraken passes the INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS value as '9999' from ADM
        Kraken passes the EC_CLOSE_BUTTON_DELAY_SECONDS value as '6' for multi page from ADM

        App level data:
        "forceViewIncentivized": false,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level setting：
        "is_skippable": false
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM5090810', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        if 'EC_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements:
            assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('18'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded not skippable, placement setting null')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_app_and_placement_not_skippable_2(self, pub_app_id):
        '''
        Kraken passes the INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS value as '9999' from ADM
        Kraken passes the EC_CLOSE_BUTTON_DELAY_SECONDS value as '6' for multi page from ADM

        App level data:
        "forceViewIncentivized": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level setting：
        "is_skippable": false,
        "multi_video_close_button_delay": null,
        "multi_ec_close_button_delay": null,
        "single_close_button_delay": null
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM509082', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        if 'EC_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements:
            assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('18'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded placement not skippable, placement setting null')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_rewarded_app_skippable_placement_not_skippable_2(self, pub_app_id):
        '''
        Kraken passes the INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS value as '9999' from ADM
        Kraken passes the EC_CLOSE_BUTTON_DELAY_SECONDS value as '6' for multi page from ADM

        App level data:
        "forceViewIncentivized": false,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level setting：
        "is_skippable": false,
        "multi_video_close_button_delay": null,
        "multi_ec_close_button_delay": null,
        "single_close_button_delay": null
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM5090820', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        if 'EC_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements:
            assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('18'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial app and placement not skippable, placement has settings')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_inter_app_skippable_placement_not_skippable(self, pub_app_id):
        '''
        Kraken passes the CLOSE_BUTTON_DELAY_SECONDS value as '9999' from ADM
        Kraken passes the EC_CLOSE_BUTTON_DELAY_SECONDS value as '6' for multi page from ADM

        App level data:
        "forceView": false,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level setting：
        "is_skippable": false,
        "multi_video_close_button_delay": 25,
        "multi_ec_close_button_delay": 26,
        "single_close_button_delay": 27
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50909', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        if 'EC_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements:
            assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('26'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial placement not skippable, placement has settings')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_inter_app_and_placement_not_skippable(self, pub_app_id):
        '''
        Kraken passes the CLOSE_BUTTON_DELAY_SECONDS value as '9999' from ADM
        Kraken passes the EC_CLOSE_BUTTON_DELAY_SECONDS value as '6' for multi page from ADM

        App level data:
        "forceView": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level setting：
        "is_skippable": false,
        "multi_video_close_button_delay": 25,
        "multi_ec_close_button_delay": 26,
        "single_close_button_delay": 27
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM509090', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        if 'EC_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements:
            assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('26'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial placment not skippable, placement no settings')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_inter_app_skippable_placement_not_skippable_1(self, pub_app_id):
        '''
        App level data:
        "forceView": false,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level setting：
        "is_skippable": false
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM509091', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        if 'EC_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements:
            assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('11'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial app and placment not skippable, placement no settings')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_inter_app_and_placement_not_skippable_1(self, pub_app_id):
        '''
        App level data:
        "forceView": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level setting：
        "is_skippable": false
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM5090910', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        if 'EC_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements:
            assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('11'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial placment not skippable, placement settings null')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_inter_app_skippable_placement_not_skippable_2(self, pub_app_id):
        '''
        App level data:
        "forceView": false,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level setting：
        "is_skippable": false,
        "multi_video_close_button_delay": null,
        "multi_ec_close_button_delay": null,
        "single_close_button_delay": null
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM509092', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        if 'EC_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements:
            assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('11'))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for interstitial app and placment not skippable, placement settings null')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_inter_app_and_placement_not_skippable_2(self, pub_app_id):
        '''
        App level data:
        "forceView": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }

        Placement level setting：
        "is_skippable": false,
        "multi_video_close_button_delay": null,
        "multi_ec_close_button_delay": null,
        "single_close_button_delay": null
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM5090920', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))
        if 'EC_CLOSE_BUTTON_DELAY_SECONDS' in normal_replacements:
            assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('11'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1345 close button pub control function for vast')
    @allure.description('Test for rewarded single page vast, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_single_placement_ctl_vast(self, pub_app_id):
        '''
        Placement level data

        "multiVideoCloseButtonDelay": 25,
        "multiECCloseButtonDelay": 26,
        "singleCloseButtonDelay": 27
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('27'))
        # PBJ-4234 change, read mutiple config
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('25'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0', 'R_1.132.0')
    @allure.story('PBJ-1345 close button pub control function for vast, '
                  'PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded single page vast, app level control, placement no setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_single_app_ctl_vast(self, pub_app_id):
        '''
        Placement level data:
        "is_skippable": true

        App level data:
        "forceViewIncentivized": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for rewarded single page vast, app level control, placement has settings')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_single_app_ctl_vast_1(self, pub_app_id):
        '''
        Placement level data:
        "is_skippable": true,
        "multi_video_close_button_delay": null,
        "multi_ec_close_button_delay": null,
        "single_close_button_delay": null

        App level data:
        "forceViewIncentivized": true,
        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSA1', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('9999'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1345 close button pub control function for vast')
    @allure.description('Test for interstitial single page, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_inter_single_placement_ctl_vast(self, pub_app_id):
        '''
        Placement level data

        "multiVideoCloseButtonDelay" : 1,
        "multiECCloseButtonDelay" : 2,
        "singleCloseButtonDelay" : 3
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916ISP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('3'))
        # PBJ-4234 change, read mutiple config
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('1'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1345 close button pub control function for vast')
    @allure.description('Test for interstitial single page, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_inter_single_app_ctl_vast(self, pub_app_id):
        '''
        App level data

        "adExperience": {
            "multiVideoCloseButtonDelay": 10,
            "multiECCloseButtonDelay": 11,
            "singleCloseButtonDelay": 12
        },
        "rewardedAdExperience": {
            "multiVideoCloseButtonDelay": 17,
            "multiECCloseButtonDelay": 18,
            "singleCloseButtonDelay": 19
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916ISA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('12'))
        # PBJ-4234 change: read multiVideoCloseButtonDelay config.
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('10'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1345 close button pub control function for vast')
    @allure.description('Test for rewarded skip after has the higher prior than close button control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_rewarded_skip_after_prior_vast(self, pub_app_id):
        '''
        Placement level: skip_after=16
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50911', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('16'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1345 close button pub control function for vast')
    @allure.description('Test for interstitial skip after has the higher prior than close button control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_inter_skip_after_prior_vast(self, pub_app_id):
        '''
        Placement level: skip_after=16
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50910', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.2', debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('16'))

    @allure.feature('normal replacements')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1377 pub side override start_muted'
                  'PBJ-4028 Server side fix for START_MUTED / sound violation in iOS SDK 6.10.1-6.10.3'
                  'PBJ-4548 [SSP] Change Start Muted Behaviour for all ad responses')
    @allure.description('Test for START_MUTED exists in both app replacement and ADM'
                        'Verify that REAL_START_MUTED is added')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.3.2', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3',
                                       'Vungle/6.11.0'])
    def test_start_muted_exist(self, pub_app_id, sdk_v):
        '''
        App level: START_MUTED = false
        ADM: START_MUTED = true
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['START_MUTED'], equal_to('false'))
        assert_that(normal_replacements['REAL_START_MUTED'], equal_to('false'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1377 pub side override start_muted'
                  'PBJ-4028 Server side fix for START_MUTED / sound violation in iOS SDK 6.10.1-6.10.3'
                  'PBJ-4548 [SSP] Change Start Muted Behaviour for all ad responses')
    @allure.description('Test for START_MUTED exists in app replacement but not exists in vast adm'
                        'Verify that REAL_START_MUTED is added')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.3.2', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3',
                                       'Vungle/6.11.0'])
    def test_start_muted_exist_vast(self, pub_app_id, sdk_v):
        '''
        App level: START_MUTED = false
        no START_MUTED in VAST adm
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['START_MUTED'], equal_to('false'))
        assert_that(normal_replacements['REAL_START_MUTED'], equal_to('false'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1377 pub side override start_muted'
                  'PBJ-4028 Server side fix for START_MUTED / sound violation in iOS SDK 6.10.1-6.10.3'
                  'PBJ-4548 [SSP] Change Start Muted Behaviour for all ad responses')
    @allure.description('Test for START_MUTED exists in app replacement but not exists in internal type adm'
                        'Verify that REAL_START_MUTED is added')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.3.2', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3',
                                       'Vungle/6.11.0'])
    def test_start_muted_exist_internal_type(self, pub_app_id, sdk_v):
        '''
        App level: START_MUTED = false
        no START_MUTED in internal mraid adm of Kraken using
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'AREYOUS82690', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['START_MUTED'], equal_to('false'))
        assert_that(normal_replacements['REAL_START_MUTED'], equal_to('false'))

    @allure.feature('normal replacements')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1377 pub side override start_muted'
                  'PBJ-4028 Server side fix for START_MUTED / sound violation in iOS SDK 6.10.1-6.10.3'
                  'PBJ-4548 [SSP] Change Start Muted Behaviour for all ad responses')
    @allure.description('Test for START_MUTED not exists in app replacement but exists in ADM'
                        'Verify that REAL_START_MUTED is added')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5e57a3a6130de800018aca0d'])
    @pytest.mark.parametrize('placement', ['DEFAULT-6818423'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.3.2', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3',
                                       'Vungle/6.11.0'])
    def test_start_muted_not_exist(self, pub_app_id, placement, sdk_v):
        '''
        App level no START_MUTED setting
        ADM: START_MUTED = true
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            sdk_version=sdk_v, debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['START_MUTED'], equal_to('true'))
        assert_that(normal_replacements['REAL_START_MUTED'], equal_to('true'))

    @allure.feature('normal replacements')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1377 pub side override start_muted'
                  'PBJ-4028 Server side fix for START_MUTED / sound violation in iOS SDK 6.10.1-6.10.3'
                  'PBJ-4548 [SSP] Change Start Muted Behaviour for all ad responses')
    @allure.description('Test for START_MUTED not exists in both app replacement and internal mraid ADM'
                        'Verify that REAL_START_MUTED is added')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5e57a3a6130de800018aca0d'])
    @pytest.mark.parametrize('placement', ['REWARDED_05_01-0855934'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.3.2', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3',
                                       'Vungle/6.11.0'])
    def test_start_muted_not_exist_internal_type(self, pub_app_id, placement, sdk_v):
        '''
        App level no START_MUTED setting
        no START_MUTED in internal mraid adm of Kraken using
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            sdk_version=sdk_v, debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(normal_replacements, 'START_MUTED')
        assert_keys_not_exist(normal_replacements, 'REAL_START_MUTED')

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1377 pub side override start_muted'
                  'PBJ-4028 Server side fix for START_MUTED / sound violation in iOS SDK 6.10.1-6.10.3'
                  'PBJ-4548 [SSP] Change Start Muted Behaviour for all ad responses')
    @allure.description('Test for START_MUTED will be added in token when VAST convert to MRAID'
                        'Verify that REAL_START_MUTED is added')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5e57a3a6130de800018aca0d'])
    @pytest.mark.parametrize('placement', ['DEFAULT-6818423'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.3.2', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3',
                                       'Vungle/6.11.0'])
    def test_start_muted_not_exist_vast(self, pub_app_id, placement, sdk_v):
        '''
        App level no START_MUTED setting
        no START_MUTED in VAST adm
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            sdk_version=sdk_v, debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['START_MUTED'], equal_to('false'))
        assert_that(normal_replacements['REAL_START_MUTED'], equal_to('false'))

    @allure.feature('normal replacements')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4548 [SSP] Change Start Muted Behaviour for all ad responses')
    @allure.description('Test for START_MUTED exists in both app replacement and ADM'
                        'Verify that REAL_START_MUTED is added')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.3.2', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3',
                                       'Vungle/6.11.0'])
    def test_start_muted_exist_android(self, pub_app_id, sdk_v):
        '''
        App level: START_MUTED = true
        ADM: START_MUTED = false
        '''
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['START_MUTED'], equal_to('true'))
        assert_that(normal_replacements['REAL_START_MUTED'], equal_to('true'))


    @allure.feature('normal replacements')
    @allure.tag('normal')
    @allure.story('PBJ-4548 [SSP] Change Start Muted Behaviour for all ad responses')
    @allure.description('Test for START_MUTED exists in both app replacement and ADM'
                        'Verify that REAL_START_MUTED is added')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.3.2', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3',
                                       'Vungle/6.11.0'])
    def test_start_muted_exist_android_e(self, pub_app_id, sdk_v):
        '''
        App level: START_MUTED = true
        ADM: START_MUTED = false
        '''
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, debug='jaeger',
                                                                        src_ip=au_ip,
                                                                        rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['START_MUTED'], equal_to('true'))
        assert_that(normal_replacements['REAL_START_MUTED'], equal_to('true'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0', 'v1.245.0')
    @allure.story('PBJ-1359 programmatic end card'
                  'PBJ-4899 Sunset customized endcard for bytedance')
    @allure.description('Verify the programmatic end card info in normal replacements')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_programmatic_end_card_info_normal_replacements(self, pub_app_id):
        '''
        End card info in vast adm:
            <![CDATA[<EndCardAdParameters>
              <cover_url>http://sf3-ttcdn-tos.pstatp.com/obj/ad.union.api/30860ab264d086db052bea3b76e17e73</cover_url>
              <icon>http://sf3-ttcdn-tos.pstatp.com/obj/web.business.image/202002135d0d86dc9a765bca41948ec9</icon>
              <app_name>疯狂猜成语-红包版</app_name>
              <description>休闲小游戏，躺着玩游戏就能赚钱，随时可以提现</description>
              <app_stars>4.5</app_stars>
              <button_text>立即下载</button_text>
              <download_url>https://www.crazyccy.com/download/ccy_csjfkccy313.apk</download_url>
            </EndCardAdParameters>]]>
        '''
        override_adm = 'seatbid.0.bid.0.adm@"<VAST version=\\"2.0\\"><Ad><InLine><AdSystem><![CDATA[Bytedance]]><\\/AdSystem><AdTitle><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\/AdTitle><Impression><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/show_event\\/?req_id=5ec796d603e1e7c01267c88fu8791&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&source_type=1&pack_time=1590630440.65&pc=OMkaunPpDyKzZarhJKk3BmafV%2FjcG%2FID2AgSFwMkc6M%3D&ttdsp_price=${AUCTION_PRICE}]]><\\/Impression><Creatives><Creative id=\\"1665015151804428\\"><Linear><Duration>00:00:46<\\/Duration><TrackingEvents><Tracking event=\\"start\\"><![CDATA[https:\\/\\/is.snssdk.com\\/api\\/ad\\/union\\/event_report\\/?event_type=4&user_timezone={timezone}&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=0]]><\\/Tracking><Tracking event=\\"complete\\"><![CDATA[https:\\/\\/is.snssdk.com\\/api\\/ad\\/union\\/event_report\\/?event_type=6&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=27]]><\\/Tracking><Tracking event=\\"creativeView\\"><![CDATA[http:\\/\\/app05.adfalcon.com\\/E\\/78c1743833b34d43991083f92bd5b392_0_b338d452-96f4-4d37-b6e1-d10de8271ff4?ev=creativeview]]><\\/Tracking><\\/TrackingEvents><VideoClicks><ClickThrough><![CDATA[https:\\/\\/events-dca.bidder.kayzen.io\\/click?ppid=313f8c39-0eb3-45ad-88ff-891559d47302&raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\/ClickThrough><ClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=1&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/ClickTracking><CustomClick id=\\"ClickCoordinates-1\\"><![CDATA[https:\\/\\/c2.gdt.qq.com\\/gdt_mclick.fcg?viewid=!s6A4zH!POBbWj7ZQJudpxTBaTzOitZ8Zrj2cUWt!HRqifXlxVXVFYsSbE41QXp8NkVBskWi5Xu3It3wZDq05WhMsgfMLVxU41AQqVoe3wHYs6zZtEO_OtSDOHBiIm_Jn3xRWbR93zoDNI2kpylT7ltMreMCvonlVZ2Br0DCTf8SQOYklg8NNwTiMJCaTcC4xb7pIVEr5A5nkmccS3H9UpiMiJTk3eT_Yn57f4UxnMy9cxrAgVDosJFLJ6rXP6tZHCWVS3kSr0l5iRK1V956hwoVlIAVZCLcI!!qfcKzeS548ctKsM2Ps6ip5M9Cpx60&jtype=0&i=1&os=2&acttype=1&s={\\"req_width\\":\\"__REQ_WIDTH__\\",\\"req_height\\":\\"__REQ_HEIGHT__\\",\\"width\\":\\"__WIDTH__\\",\\"height\\":\\"__HEIGHT__\\",\\"down_x\\":\\"__DOWN_X__\\",\\"down_y\\":\\"__DOWN_Y__\\",\\"up_x\\":\\"__UP_X__\\",\\"up_y\\":\\"__UP_Y__\\"}&lpp=click_ext=eyJleHBfcGFyYW0iOiJjYXJyaWVyX2VuYWJsZToyIn0=&clklpp=__CLICK_LPP__&nxjp=1&cdnxj=1&xp=1&tl=1]]><\\/CustomClick><CustomClick id=\\"ClickCoordinates-2\\"><![CDATA[http:\\/\\/link\\/to\\/customclick\\/2]]><\\/CustomClick><CustomClick id=\\"customclick-3\\"><![CDATA[http:\\/\\/link\\/to\\/customclick\\/3]]><\\/CustomClick><\\/VideoClicks><MediaFiles><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[ asdjfklajsd;fkja;sdlkfjklasdjfklasdjfkl.mp4 ]]><\\/MediaFile><MediaFile bitrate=\\"206\\" delivery=\\"progressive\\" height=\\"180\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"320\\"><![CDATA[ test\\/jsldfjlksdfjk.mp4 ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[ v3-ad.ixigua.com\\/kghkhk\\/toutiao123werwerew.abc ]]><\\/MediaFile><MediaFile bitrate=\\"56\\" delivery=\\"progressive\\" height=\\"144\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"176\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/17\\/source\\/doubleclick_dmm\\/ctier\\/L\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748511\\/sparams\\/id,itag,source,ctier,ip,ipbits,expire\\/signature\\/8044BE9E3E1793FF36C03998BA13848E7C845ABE.75B6CAFBF57F6F96C78BDFCEB9653E601FD7E8D8\\/key\\/ck2\\/file\\/file.3gpp ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[https:\\/\\/v3-ad.ixigua.com\\/kghkhk\\/toutiao123]]><\\/MediaFile><MediaFile bitrate=\\"206\\" delivery=\\"progressive\\" height=\\"180\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"320\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/36\\/source\\/doubleclick_dmm\\/ctier\\/L\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748512\\/sparams\\/id,itag,source,ctier,ip,ipbits,expire\\/signature\\/29EC5A3574F0873D71FF75DEA54B89FD30A0D0B1.82B0C3EBBBAF7046A8DFBF3D94AAD9FC69C5C9A4\\/key\\/ck2\\/file\\/file.3gpp ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[https:\\/\\/cdn-cn.vungle.cn\\/zen\\/497a5dead8498d62d7c65967729639f7-1280x720-Q2.mp4]]><\\/MediaFile><MediaFile bitrate=\\"372\\" delivery=\\"progressive\\" height=\\"360\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/mp4\\" width=\\"640\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/18\\/source\\/doubleclick_dmm\\/ctier\\/L\\/acao\\/yes\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748513\\/sparams\\/id,itag,source,ctier,acao,ip,ipbits,expire\\/signature\\/484784AD6E9C1516EC07970AB978D11555654A9A.57EFB4F5F3CCE7F30CFBA1951E6434319300BE12\\/key\\/ck2\\/file\\/file.mp4 ]]><\\/MediaFile><MediaFile bitrate=\\"1879\\" delivery=\\"progressive\\" height=\\"720\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/mp4\\" width=\\"1280\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/22\\/source\\/doubleclick_dmm\\/ctier\\/L\\/acao\\/yes\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748528\\/sparams\\/id,itag,source,ctier,acao,ip,ipbits,expire\\/signature\\/7136B1FF2CD283E5A90276E455C5F970B91A35FF.8E6707BA3249059D7BA09F6E3D59FF6BA1D78FE0\\/key\\/ck2\\/file\\/file.mp4 ]]><\\/MediaFile><\\/MediaFiles><\\/Linear><\\/Creative><Creative><CompanionAds><Companion id=\\"post-roll\\" width=\\"1280\\" height=\\"720\\"><CompanionClickThrough><![CDATA[https:\\/\\/events-dca.bidder.kayzen.io\\/click?raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\/CompanionClickThrough><CompanionClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=2&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/CompanionClickTracking><TrackingEvents><Tracking event=\\"creativeView\\"><\\/Tracking><\\/TrackingEvents><StaticResource creativeType=\\"image\\/jpeg\\"><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/obj\\/mosaic-legacy\\/2ff3f000e60c223e67984]]><\\/StaticResource><\\/Companion><Companion id=\\"vungle_endcard_v1\\"><CompanionClickThrough><![CDATA[https:\\/\\/events-dca.bidder.kayzen.io\\/click?raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\/CompanionClickThrough><CompanionClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=2&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/CompanionClickTracking><TrackingEvents><\\/TrackingEvents><AdParameters xmlEncoded=\\"true\\"><![CDATA[<EndCardAdParameters><icon>https:\\/\\/p3-tt.byteimg.com\\/img\\/ad.union.api\\/7c51525c9163b92843a26bf89aaded1f~100x100.image<\\/icon><app_name>\\u70B9\\u4EAE\\u57CE\\u5E02-\\u5168\\u7F51\\u5F00\\u670D<\\/app_name><cover_url>https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/mosaic-legacy\\/2ff3f000e60c223e67984~noop.jpg<\\/cover_url><app_stars>5<\\/app_stars><button_text>\\u70B9\\u51FB\\u4E0B\\u8F7D<\\/button_text><download_url>https%3A%2F%2Fwww.crazyccy.com%2Fdownload%2Fccy_csjfkccy313.apk<\\/download_url><description>\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417<\\/description><\\/EndCardAdParameters>]]><\\/AdParameters><\\/Companion><\\/CompanionAds><\\/Creative><\\/Creatives><Description><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\/Description><Survey><\\/Survey><Extensions><Extension type=\\"AdVerifications\\"><AdVerifications><Verification vendor=\\"moat.com-omsdkvungleinappvideo781943494431\\"><JavaScriptResource apiFramework=\\"omid\\" browserOptional=\\"true\\"><![CDATA[https:\\/\\/z.moatads.com\\/omsdkvungleinappvideo781943494431\\/moatvideo.js]]><\\/JavaScriptResource><VerificationParameters><![CDATA[{\\"moatClientLevel1\\":\\"{{{app_id}}}\\",\\"moatClientLevel2\\":\\"{{{campaign_id}}}\\",\\"moatClientLevel3\\":\\"{{{creative_id}}}\\",\\"moatClientLevel4\\":\\"{{{placement_id}}}\\",\\"moatClientSlicer1\\":\\"{{{pub_app_id}}}\\",\\"moatClientLevel5\\":\\"{{{rtb_deal_id}}}\\",\\"moatClientLevel6\\":\\"{{{rtb_connection_id}}}\\"}]]><\\/VerificationParameters><\\/Verification><\\/AdVerifications><\\/Extension><Extension type=\\"Extra\\"><CTA><![CDATA[\\u70B9\\u51FB\\u4E0B\\u8F7D]]><\\/CTA><SystemIcon><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/07c04164de3140d2cfe4bdd9812aef22~c1_0x0_q100.png]]><\\/SystemIcon><FullStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/48c275deda9f2daa92acccf8218fc59f~c1_0x0_q100.jpeg]]><\\/FullStar><HalfStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/b273598ab25fec09a467d2b895e3c53e~c1_0x0_q100.jpeg]]><\\/HalfStar><EmptyStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/fedbae142b79804e383eed3f4d06e9d5~c1_0x0_q100.jpeg]]><\\/EmptyStar><Review><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/297845a2690ec96bd1290a0a289ab373~c1_0x0_q100.jpeg]]><\\/Review><MoPubCtaText><\\/MoPubCtaText><\\/Extension><\\/Extensions><\\/InLine><\\/Ad><\\/VAST>"'
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb,
                                                                        override_bid_response_any=override_adm))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm'] and 'templateSettings' in ad_markup:
            normal_replacements = ad_markup['templateSettings']['normal_replacements']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_keys_not_exist(normal_replacements, 'APP_NAME')
            assert_keys_not_exist(normal_replacements, 'APP_DESCRIPTION')
            assert_keys_not_exist(normal_replacements, 'APP_RATING')
            assert_keys_not_exist(normal_replacements, 'CTA_BUTTON_TEXT')
            assert_keys_exist(normal_replacements, 'EC_CTA_URL')

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1393 close button delay experiment for programmatic')
    @allure.description('Test for experiment setting override placement level close button delay setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_close_button_delay_experiment_vast(self, pub_app_id):
        '''
        The experiment has been removed from code

        Placement level data

        "multiVideoCloseButtonDelay" : 1,
        "multiECCloseButtonDelay" : 2,
        "singleCloseButtonDelay" : 3

        Ad duration: 27s
        Experiment: 50%
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916ISP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            sdk_version='Vungle/6.3.2', debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast, src_ip=jp_ip,
            experiment='Close_Delay_JP=Test4Issue'))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('3'))
        # PBJ-4234 change, read mutiple config
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('1'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1393 close button delay experiment for programmatic')
    @allure.description('Test for experiment setting override placement level skip after setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_close_button_delay_experiment_vast_1(self, pub_app_id):
        '''
        The experiment has been removed from code

        Placement level: skip_after=16

        Ad duration: 27s
        Experiment: 50%
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50910', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            sdk_version='Vungle/6.3.2', debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast, src_ip=jp_ip,
            experiment='Close_Delay_JP=Test4Issue'))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('16'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1393 close button delay experiment for programmatic')
    @allure.description('Test for experiment does not support vast rewarded ad')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_close_button_delay_experiment_not_support_rewarded_vast(self, pub_app_id):
        '''
        Placement level data

        "multiVideoCloseButtonDelay": 25,
        "multiECCloseButtonDelay": 26,
        "singleCloseButtonDelay": 27
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            sdk_version='Vungle/6.3.2', debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast, src_ip=jp_ip,
            experiment='Close_Delay_JP=Test4Issue'))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('27'))
        # PBJ-4234 change, use mutiple config
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('25'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1393 close button delay experiment for programmatic')
    @allure.description('Test for experiment does not support internal rewarded ad')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_close_button_delay_experiment_not_support_internal_rewarded(self, pub_app_id):
        '''
        Placement level data

        "multiVideoCloseButtonDelay": 25,
        "multiECCloseButtonDelay": 26,
        "singleCloseButtonDelay": 27
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            sdk_version='Vungle/6.3.2', debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1, src_ip=jp_ip,
            experiment='Close_Delay_JP=Test4Issue'))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('27'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1393 close button delay experiment for programmatic')
    @allure.description('Test for experiment does not support internal interstitial ad')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_close_button_delay_experiment_not_support_internal_interstitial(self, pub_app_id):
        '''
        Placement level data

        "multiVideoCloseButtonDelay" : 1,
        "multiECCloseButtonDelay" : 2,
        "singleCloseButtonDelay" : 3
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916ISP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            sdk_version='Vungle/6.3.2', debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1, src_ip=jp_ip,
            experiment='Close_Delay_JP=Test4Issue'))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['CLOSE_BUTTON_DELAY_SECONDS'], equal_to('3'))

    # ----------------------------------------- Hidden timer ctl start -----------------------------------------

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, rewarded single page, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_rewarded_single_placement_ctl(self, pub_app_id):
        '''
        Placement level data

        "hidden_timer": {
            "is_override": true,
            "show_multi_ec_close_button_countdown": false,
            "show_multi_video_close_button_countdown": false,
            "show_single_close_button_countdown": false
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_CLOSE_BUTTON_COUNTDOWN'], equal_to('false'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, rewarded multi page with end card, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_rewarded_multi_placement_ctl(self, pub_app_id):
        '''
        Placement level data

        "hidden_timer": {
            "is_override": true,
            "show_multi_ec_close_button_countdown": false,
            "show_multi_video_close_button_countdown": false,
            "show_single_close_button_countdown": false
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RMP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN'], equal_to('false'))
        assert_that(normal_replacements['SHOW_EC_CLOSE_BUTTON_COUNTDOWN'], equal_to('false'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, rewarded single page, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_rewarded_single_app_ctl(self, pub_app_id):
        '''
        App level data

        "hiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        },
        "rewardedHiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, rewarded multi page with end card, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_rewarded_multi_app_ctl(self, pub_app_id):
        '''
        App level data

        "hiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        },
        "rewardedHiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RMA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))
        assert_that(normal_replacements['SHOW_EC_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, interstitial single page, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_inter_single_placement_ctl(self, pub_app_id):
        '''
        Placement level data

        "hidden_timer": {
            "is_override": true,
            "show_multi_ec_close_button_countdown": false,
            "show_multi_video_close_button_countdown": false,
            "show_single_close_button_countdown": false
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916ISP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_CLOSE_BUTTON_COUNTDOWN'], equal_to('false'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, interstitial multi page with end card, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_inter_multi_placement_ctl(self, pub_app_id):
        '''
        Placement level data

        "hidden_timer": {
            "is_override": true,
            "show_multi_ec_close_button_countdown": false,
            "show_multi_video_close_button_countdown": false,
            "show_single_close_button_countdown": false
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916IMP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN'], equal_to('false'))
        assert_that(normal_replacements['SHOW_EC_CLOSE_BUTTON_COUNTDOWN'], equal_to('false'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, interstitial single page, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_inter_single_app_ctl(self, pub_app_id):
        '''
        App level data

        "hiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        },
        "rewardedHiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916ISA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, interstitial multi page with end card, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_inter_multi_app_ctl(self, pub_app_id):
        '''
        App level data

        "hiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        },
        "rewardedHiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916IMA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))
        assert_that(normal_replacements['SHOW_EC_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, single page, no setting in placement level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_single_no_placement_setting(self, pub_app_id):
        '''
        App level data

        "hiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        },
        "rewardedHiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'AREYOUS82690', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, multi page, no setting in placement level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hidden_timer_multi_no_placement_setting_1(self, pub_app_id, placement):
        '''
        App level data

        "hiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        },
        "rewardedHiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))
        assert_that(normal_replacements['SHOW_EC_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, ext vast single page, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_rewarded_single_placement_ctl_vast(self, pub_app_id):
        '''
        Placement level data

        "hidden_timer": {
            "is_override": true,
            "show_multi_ec_close_button_countdown": false,
            "show_multi_video_close_button_countdown": false,
            "show_single_close_button_countdown": false
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # PBJ-4234 update
        # assert_that(normal_replacements['SHOW_CLOSE_BUTTON_COUNTDOWN'], equal_to('false'))
        assert_that(normal_replacements['SHOW_EC_CLOSE_BUTTON_COUNTDOWN'], equal_to('false'))
        assert_that(normal_replacements['SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN'], equal_to('false'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, ext vast multi page with end card, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_rewarded_multi_placement_ctl_vast(self, pub_app_id):
        '''
        Placement level data

        "hidden_timer": {
            "is_override": true,
            "show_multi_ec_close_button_countdown": false,
            "show_multi_video_close_button_countdown": false,
            "show_single_close_button_countdown": false
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RMP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN'], equal_to('false'))
        assert_that(normal_replacements['SHOW_EC_CLOSE_BUTTON_COUNTDOWN'], equal_to('false'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, ext vast single page, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_rewarded_single_app_ctl_vast(self, pub_app_id):
        '''
        App level data

        "hiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        },
        "rewardedHiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # PBJ-4234 update
        assert_that(normal_replacements['SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))
        assert_that(normal_replacements['SHOW_EC_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, ext vast multi page with end card, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_rewarded_multi_app_ctl_vast(self, pub_app_id):
        '''
        App level data

        "hiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        },
        "rewardedHiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RMA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))
        assert_that(normal_replacements['SHOW_EC_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, vast single page, no setting in placement level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hidden_timer_single_no_placement_setting_vast(self, pub_app_id):
        '''
        App level data

        "hiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        },
        "rewardedHiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'AREYOUS82690', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # PBJ-4234 update
        # assert_that(normal_replacements['SHOW_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))
        assert_that(normal_replacements['SHOW_EC_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))
        assert_that(normal_replacements['SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))

    @allure.feature('hidden timer control')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1553 Hidden timer controls')
    @allure.description('Test for hidden timer control, vast multi page, no setting in placement level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hidden_timer_multi_no_placement_setting_vast(self, pub_app_id, placement):
        '''
        App level data

        "hiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        },
        "rewardedHiddenTimer": {
            "show_multi_ec_close_button_countdown": true,
            "show_multi_video_close_button_countdown": true,
            "show_single_close_button_countdown": true
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))
        assert_that(normal_replacements['SHOW_EC_CLOSE_BUTTON_COUNTDOWN'], equal_to('true'))

    # ----------------------------------------- Hidden timer ctl end -----------------------------------------

    @allure.feature('fullscreen clickable')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1666 Verify full screen clickable is default to enable for programmatic vung_mraid ads.')
    @allure.description('Test for fullscreen clickable - app flag true, placement flag false, vast')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [full_screen_clickable_app_t])
    def test_fullscreen_clickable_vast_app_t_placement_f(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, full_screen_clickable_app_t_placement_f_mraid,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        template_settings = ad_markup['templateSettings']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(template_settings['normal_replacements']['FULL_CTA'], True)

    @allure.feature('fullscreen clickable')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1666 Verify full screen clickable is default to enable for programmatic vung_mraid ads.')
    @allure.description('Test for fullscreen clickable - app flag true, placement no flag, vast')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [full_screen_clickable_app_t])
    def test_fullscreen_clickable_vast_app_t_placement_n(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, full_screen_clickable_app_t_placement_n,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        template_settings = ad_markup['templateSettings']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(template_settings['normal_replacements']['FULL_CTA'], True)

    @allure.feature('fullscreen clickable')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1666 Verify full screen clickable is default to enable for programmatic vung_mraid ads.')
    @allure.description('Test for fullscreen clickable - app flag false, placement flag true, vast')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [full_screen_clickable_app_f])
    def test_fullscreen_clickable_vast_app_f_placement_t(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, full_screen_clickable_app_f_placement_t_mraid,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        template_settings = ad_markup['templateSettings']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(template_settings['normal_replacements']['FULL_CTA'], True)

    @allure.feature('fullscreen clickable')
    @allure.tag('normal', 'test_mode', 'R_1.128.0')
    @allure.story('PBJ-1666 Verify full screen clickable is default to enable for programmatic vung_mraid ads.')
    @allure.description('Test for fullscreen clickable - app flag false, placement no flag, vast')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [full_screen_clickable_app_f])
    def test_fullscreen_clickable_vast_app_f_placement_n(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, full_screen_clickable_app_f_placement_n,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        template_settings = ad_markup['templateSettings']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(template_settings['normal_replacements']['FULL_CTA'], True)

    # ------------------------------------------------- ASOI begins ---------------------------------------------------

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for rewarded single page full screen, app level control, placement no setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_asoi_rewarded_single_no_placement_setting(self, pub_app_id):
        '''
        App level data:
        "asoi_setting_rewarded": "aggressive",
        "asoi_setting": "complete"

        Placement level no setting
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('aggressive'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for rewarded single page full screen, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_asoi_rewarded_single_app_ctl(self, pub_app_id):
        '''
        App level data:
        "asoi_setting_rewarded": "aggressive"

        Placement level data:
        "asoi_is_override": false,
        "asoi_setting": "complete"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('aggressive'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for rewarded single page full screen, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_asoi_rewarded_single_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "asoi_setting_rewarded": "aggressive"

        Placement level data:
        "asoi_is_override": true,
        "asoi_setting": "complete"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RSP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('complete'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for rewarded multi page full screen, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_asoi_rewarded_multi_app_ctl(self, pub_app_id):
        '''
        App level data:
        "asoi_setting_rewarded": "aggressive"

        Placement level data:
        "asoi_is_override": false,
        "asoi_setting": "complete"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RMA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('aggressive'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for rewarded multi page full screen, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_asoi_rewarded_multi_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "asoi_setting_rewarded": "aggressive"

        Placement level data:
        "asoi_is_override": true,
        "asoi_setting": "off"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RMP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('off'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for interstitial single page full screen, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_asoi_inter_single_app_ctl(self, pub_app_id):
        '''
        App level data:
        "asoi_setting": "complete"

        Placement level data:
        "asoi_is_override": false,
        "asoi_setting": "aggressive"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916ISA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('complete'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for interstitial single page full screen, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_asoi_inter_single_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "asoi_setting": "complete"

        Placement level data:
        "asoi_is_override": true,
        "asoi_setting": "aggressive"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916ISP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('aggressive'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for interstitial multi page full screen, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_asoi_inter_multi_app_ctl(self, pub_app_id):
        '''
        App level data:
        "asoi_setting": "complete"

        Placement level data:
        "asoi_is_override": false,
        "asoi_setting": "off"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916IMA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('complete'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for interstitial multi page full screen, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_asoi_inter_multi_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "asoi_setting": "complete"

        Placement level data:
            "asoi_is_override": true,
            "asoi_setting": "off"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916IMP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('off'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for vast, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_asoi_vast_no_placement_setting(self, pub_app_id):
        '''
        App level data:
        "asoi_setting_rewarded": "aggressive",
        "asoi_setting": "complete"

        Placement level no setting
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('aggressive'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for vast, app level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_asoi_vast_app_ctl(self, pub_app_id):
        '''
        App level data:
        "asoi_setting_rewarded": "aggressive",
        "asoi_setting": "complete"

        Placement level data:
        "asoi_is_override": false,
        "asoi_setting": "off"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916IMA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('complete'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for vast, placement level control')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_asoi_vast_placement_ctl(self, pub_app_id):
        '''
        App level data:
        "asoi_setting_rewarded": "aggressive",
        "asoi_setting": "complete"

        Placement level data:
        "asoi_is_override": true,
        "asoi_setting": "off"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916RMP', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('off'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for no both app and placement level control on ASOI')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_asoi_no_app_and_placement_setting(self, pub_app_id):
        '''
        App level no setting

        Placement level no setting
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement_1, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(normal_replacements, 'ASOI_SETTINGS')

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for no app level control on ASOI, rewarded placement override')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_asoi_no_app_setting_rewarded_placement_override(self, pub_app_id):
        '''
        App level no setting

        Placement level data:
        "asoi_is_override": true,
        "asoi_setting": "off"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM509080', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('off'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for no app level control on ASOI, rewarded placement not override')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_asoi_no_app_setting_rewarded_placement_not_override(self, pub_app_id):
        '''
        App level no setting

        Placement level data:
        "asoi_is_override": false,
        "asoi_setting": "aggressive"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM5090810', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(normal_replacements, 'ASOI_SETTINGS')

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for no app level control on ASOI, interstitial placement override')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_asoi_no_app_setting_inter_placement_override(self, pub_app_id):
        '''
        App level no setting

        Placement level data:
        "asoi_is_override": true,
        "asoi_setting": "aggressive"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM5090910', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('aggressive'))

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for no app level control on ASOI, interstitial placement not override')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_asoi_no_app_setting_inter_placement_not_override(self, pub_app_id):
        '''
        App level no setting

        Placement level data:
        "asoi_is_override": false,
        "asoi_setting": "complete"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM509090', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(normal_replacements, 'ASOI_SETTINGS')

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for no app level control on ASOI, rewarded placement not override')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_asoi_vast_no_app_setting_rewarded_placement_not_override(self, pub_app_id):
        '''
        App level no setting

        Placement level data:
        "asoi_is_override": false,
        "asoi_setting": "aggressive"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM5090810', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(normal_replacements, 'ASOI_SETTINGS')

    @allure.feature('asoi')
    @allure.tag('normal', 'test_mode', 'R_1.134.0', 'ad_format')
    @allure.story('PBJ-1783 ASOI pub control')
    @allure.description('Test for no app level control on ASOI, interstitial placement override')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_asoi_vast_no_app_setting_inter_placement_override(self, pub_app_id):
        '''
        App level no setting

        Placement level data:
        "asoi_is_override": true,
        "asoi_setting": "aggressive"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM5090910', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['ASOI_SETTINGS'], equal_to('aggressive'))

    # ------------------------------------------------- SKOverlay begins --------------------------------------------------

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-2064 Add SKOverlay/SKProductionView control in the ad server(jaeger)')
    @allure.description('Test for Jaeger pass the storekit tokens following the app level setting, no setting in adm')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_skoverlay_app_setting_1(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "product_view",
            "asoi_complete": "overlay_view",
            "cta_only": "off"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_FSC'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_AGGRESSIVE'], equal_to('product_view'))
        assert_that(normal_replacements['SK_ASOI_COMPLETE'], equal_to('overlay_view'))
        assert_that(normal_replacements['SK_CTA_ONLY'], equal_to('off'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-2064 Add SKOverlay/SKProductionView control in the ad server(jaeger)')
    @allure.description('Test for Jaeger pass the storekit tokens following the app level setting, no setting in adm')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_skoverlay_app_setting_2(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "default",
            "asoi_complete": "default",
            "cta_only": "default"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_FSC'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_AGGRESSIVE'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_COMPLETE'], equal_to('default'))
        assert_that(normal_replacements['SK_CTA_ONLY'], equal_to('default'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-2064 Add SKOverlay/SKProductionView control in the ad server(jaeger)')
    @allure.description('Test for app level setting override the creative level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_skoverlay_app_setting_override_1(self, pub_app_id, placement):
        '''
        App level setting:
        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "product_view",
            "asoi_complete": "overlay_view",
            "cta_only": "off"
        }

        Setting in ADM:
          "SK_CTA_ONLY": "product_view",
          "SK_ASOI_COMPLETE": "off",
          "SK_ASOI_AGGRESSIVE": "default",
          "SK_FSC": "overlay_view"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_FSC'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_AGGRESSIVE'], equal_to('product_view'))
        assert_that(normal_replacements['SK_ASOI_COMPLETE'], equal_to('overlay_view'))
        assert_that(normal_replacements['SK_CTA_ONLY'], equal_to('off'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-2064 Add SKOverlay/SKProductionView control in the ad server(jaeger)')
    @allure.description('Test for app level setting override the creative level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_skoverlay_app_setting_override_2(self, pub_app_id, placement):
        '''
        App level setting:
        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "default",
            "asoi_complete": "default",
            "cta_only": "default"
        }

        Setting in ADM:
          "SK_CTA_ONLY": "product_view",
          "SK_ASOI_COMPLETE": "off",
          "SK_ASOI_AGGRESSIVE": "default",
          "SK_FSC": "overlay_view"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_FSC'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_AGGRESSIVE'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_COMPLETE'], equal_to('default'))
        assert_that(normal_replacements['SK_CTA_ONLY'], equal_to('default'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-2064 Add SKOverlay/SKProductionView control in the ad server(jaeger)')
    @allure.description('Test for Jaeger pass creative level setting if no setting in app level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['DEFAULT02024'])
    def test_skoverlay_pass_creative_setting(self, pub_app_id, placement):
        '''
        App level no setting

        Setting in ADM:
          "SK_CTA_ONLY": "product_view",
          "SK_ASOI_COMPLETE": "off",
          "SK_ASOI_AGGRESSIVE": "default",
          "SK_FSC": "overlay_view"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_FSC'], equal_to('overlay_view'))
        assert_that(normal_replacements['SK_ASOI_AGGRESSIVE'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_COMPLETE'], equal_to('off'))
        assert_that(normal_replacements['SK_CTA_ONLY'], equal_to('product_view'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-2064 Add SKOverlay/SKProductionView control in the ad server(jaeger)')
    @allure.description('Test for the case of no setting from both app level and adm in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['AREYOUS82694'])
    def test_skoverlay_no_app_setting_test_mode(self, pub_app_id, placement):
        '''
        App level and ADM no setting
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(normal_replacements, 'SK_FSC')
        assert_keys_not_exist(normal_replacements, 'SK_ASOI_AGGRESSIVE')
        assert_keys_not_exist(normal_replacements, 'SK_ASOI_COMPLETE')
        assert_keys_not_exist(normal_replacements, 'SK_CTA_ONLY')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-2278 Support SKDT SKOverlay updates in ad server - Jaeger')
    @allure.description('Test for Jaeger passes the SKDT tokens following the app level setting, test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_skdt_app_setting_test_mode_1(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "skdt": "default"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_SKDT'], equal_to('default'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-2278 Support SKDT SKOverlay updates in ad server - Jaeger')
    @allure.description('Test for Jaeger passes the SKDT tokens following the app level setting, test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_skdt_app_setting_test_mode_2(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "skdt": "product_view"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_SKDT'], equal_to('product_view'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-2278 Support SKDT SKOverlay updates in ad server - Jaeger')
    @allure.description('Test for Jaeger passes the SKDT tokens following the app level setting, test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_t])
    @pytest.mark.parametrize('placement', [common_test_placement_t])
    def test_skdt_app_setting_test_mode_3(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "skdt": "overlay_view"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_SKDT'], equal_to('overlay_view'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-2278 Support SKDT SKOverlay updates in ad server - Jaeger')
    @allure.description('Test for Jaeger does not pass the SKDT tokens if there is no app level setting, test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['AREYOUS82694'])
    def test_skdt_no_app_setting_test_mode(self, pub_app_id, placement):
        '''
        App level and ADM no setting
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(normal_replacements, 'SK_SKDT')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-2278 Support SKDT SKOverlay updates in ad server - Jaeger')
    @allure.description('Test for Jaeger passes the SKDT tokens following the app level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_skdt_app_setting_1(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "skdt": "default"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_SKDT'], equal_to('default'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-2278 Support SKDT SKOverlay updates in ad server - Jaeger')
    @allure.description('Test for Jaeger passes the SKDT tokens following the app level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_skdt_app_setting_2(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "skdt": "product_view"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_SKDT'], equal_to('product_view'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-2278 Support SKDT SKOverlay updates in ad server - Jaeger')
    @allure.description('Test for Jaeger passes the SKDT tokens following the app level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b5'])
    @pytest.mark.parametrize('placement', ['DEFAULT02025'])
    def test_skdt_app_setting_3(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "skdt": "overlay_view"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_SKDT'], equal_to('overlay_view'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-2278 Support SKDT SKOverlay updates in ad server - Jaeger')
    @allure.description('Test for Jaeger does not pass the SKDT tokens if there is no app level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['AREYOUS82694'])
    def test_skdt_no_app_setting(self, pub_app_id, placement):
        """
        App level and ADM no setting
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(normal_replacements, 'SK_SKDT')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3366 Support SKoverlay control for the iOS apps on app and placement level'
                  'PBJ-3399 Set FULL_CTA token for IOS request.')
    @allure.description("Test template token value for there is fullScreenClickable setting in app level and "
                        "fullScreenClickable =inherit in placement level")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids, non_test_mode_kraken_rtb_ids])
    def test_skoverlay_config_app_setting_fsc_on(self, pub_app_id, placement, rtb):
        """
        App level setting
        fullscreenClickable:fsc_off

        placement level setting
        fullscreenClickable: inherit
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(normal_replacements, 'FULL_CTA_OPTION')
        assert_keys_exist(normal_replacements, 'FULL_CTA')
        assert_that(normal_replacements['FULL_CTA_OPTION'], 'fsc_off')
        assert_that(normal_replacements['FULL_CTA'], equal_to('false'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for Jaeger pass the storekit tokens following the app level setting, no setting in adm'
                        'for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_skoverlay_app_setting_1e(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "product_view",
            "asoi_complete": "overlay_view",
            "cta_only": "off"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0', src_ip=au_ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_FSC'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_AGGRESSIVE'], equal_to('product_view'))
        assert_that(normal_replacements['SK_ASOI_COMPLETE'], equal_to('overlay_view'))
        assert_that(normal_replacements['SK_CTA_ONLY'], equal_to('off'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for Jaeger pass the storekit tokens following the app level setting, no setting in adm'
                        'for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_skoverlay_app_setting_2e(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "default",
            "asoi_complete": "default",
            "cta_only": "default"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0', src_ip=au_ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_FSC'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_AGGRESSIVE'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_COMPLETE'], equal_to('default'))
        assert_that(normal_replacements['SK_CTA_ONLY'], equal_to('default'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for app level setting override the creative level setting for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_skoverlay_app_setting_override_1e(self, pub_app_id, placement):
        '''
        App level setting:
        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "product_view",
            "asoi_complete": "overlay_view",
            "cta_only": "off"
        }

        Setting in ADM:
          "SK_CTA_ONLY": "product_view",
          "SK_ASOI_COMPLETE": "off",
          "SK_ASOI_AGGRESSIVE": "default",
          "SK_FSC": "overlay_view"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_FSC'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_AGGRESSIVE'], equal_to('product_view'))
        assert_that(normal_replacements['SK_ASOI_COMPLETE'], equal_to('overlay_view'))
        assert_that(normal_replacements['SK_CTA_ONLY'], equal_to('off'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for app level setting override the creative level setting for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_skoverlay_app_setting_override_2e(self, pub_app_id, placement):
        '''
        App level setting:
        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "default",
            "asoi_complete": "default",
            "cta_only": "default"
        }

        Setting in ADM:
          "SK_CTA_ONLY": "product_view",
          "SK_ASOI_COMPLETE": "off",
          "SK_ASOI_AGGRESSIVE": "default",
          "SK_FSC": "overlay_view"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_FSC'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_AGGRESSIVE'], equal_to('default'))
        assert_that(normal_replacements['SK_ASOI_COMPLETE'], equal_to('default'))
        assert_that(normal_replacements['SK_CTA_ONLY'], equal_to('default'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for the case of no setting from both app level and adm in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['AREYOUS82694'])
    def test_skoverlay_no_app_setting_test_mode_e(self, pub_app_id, placement):
        '''
        App level and ADM no setting
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(normal_replacements, 'SK_FSC')
        assert_keys_not_exist(normal_replacements, 'SK_ASOI_AGGRESSIVE')
        assert_keys_not_exist(normal_replacements, 'SK_ASOI_COMPLETE')
        assert_keys_not_exist(normal_replacements, 'SK_CTA_ONLY')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for Jaeger passes the SKDT tokens following the app level setting for eDSP, test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_skdt_app_setting_test_mode_1e(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "skdt": "default"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_SKDT'], equal_to('default'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for Jaeger passes the SKDT tokens following the app level setting for eDSP, test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_skdt_app_setting_test_mode_2e(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "skdt": "product_view"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_SKDT'], equal_to('product_view'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for Jaeger passes the SKDT tokens following the app level setting for eDSP, test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_t])
    @pytest.mark.parametrize('placement', [common_test_placement_t])
    def test_skdt_app_setting_test_mode_3e(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "skdt": "overlay_view"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.8.0',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_SKDT'], equal_to('overlay_view'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'test_mode')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for Jaeger does not pass the SKDT tokens if there is no app level setting for eDSP, '
                        'test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['AREYOUS82694'])
    def test_skdt_no_app_setting_test_mode_e(self, pub_app_id, placement):
        '''
        App level and ADM no setting
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='Vungle/6.8.0',
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(normal_replacements, 'SK_SKDT')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for Jaeger passes the SKDT tokens following the app level setting for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_skdt_app_setting_1e(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "skdt": "default"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='Vungle/6.8.0', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_SKDT'], equal_to('default'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for Jaeger passes the SKDT tokens following the app level setting for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_skdt_app_setting_2e(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "skdt": "product_view"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='Vungle/6.8.0', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_SKDT'], equal_to('product_view'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for Jaeger passes the SKDT tokens following the app level setting for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b5'])
    @pytest.mark.parametrize('placement', ['DEFAULT02025'])
    def test_skdt_app_setting_3e(self, pub_app_id, placement):
        '''
        App level setting:

        "storekit": {
            "skdt": "overlay_view"
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='Vungle/6.8.0', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(normal_replacements['SK_SKDT'], equal_to('overlay_view'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for Jaeger does not pass the SKDT tokens if there is no app level setting for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['AREYOUS82694'])
    def test_skdt_no_app_setting_e(self, pub_app_id, placement):
        """
        App level and ADM no setting
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='Vungle/6.8.0', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(normal_replacements, 'SK_SKDT')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3366 Support SKoverlay control for the iOS apps on app and placement level'
                  'PBJ-3399 Set FULL_CTA token for IOS request.')
    @allure.description("Test template token value for there is fullScreenClickable setting in app level and "
                        "fullScreenClickable =inherit in placement level for eDSP")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_skoverlay_config_app_setting_fsc_on_e(self, pub_app_id, placement, rtb):
        """
        App level setting
        fullscreenClickable:fsc_off

        placement level setting
        fullscreenClickable: inherit
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(normal_replacements, 'FULL_CTA_OPTION')
        assert_keys_exist(normal_replacements, 'FULL_CTA')
        assert_that(normal_replacements['FULL_CTA_OPTION'], 'fsc_off')
        assert_that(normal_replacements['FULL_CTA'], equal_to('false'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify jaeger server no sko in bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_no_sko_in_bid_response_for_liftoff(self, pub_app_id, placement, rtb):
        """
        App level setting
        fullscreenClickable:fsc_off

        placement level setting
        fullscreenClickable: inherit
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                          rtb_selector=rtb))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'campaign')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify jaeger will not server empty skoverlay object in bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_empty_sko_in_bid_response_for_liftoff(self, pub_app_id, placement, rtb):

        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {}
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                          override_bid_ext=json.dumps(override_bid_ext),
                                          rtb_selector=rtb))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify SKOVERLAY_AUTO='true' when show =1 in bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_01(self, pub_app_id, placement, rtb):
        """
            App level setting
            fullscreenClickable:"fsc_off"

            placement level setting
            fullscreenClickable:"inhert"
           """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {"show": 1}
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', override_bid_ext=json.dumps(override_bid_ext),
                                          rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, "SKOVERLAY_AUTO")
        # below are checking default value
        assert_that(normal_replacements["SKOVERLAY_DELAY_SECONDS"], equal_to("0"))
        assert_that(normal_replacements["SKOVERLAY_AUTO_CLOSE"], equal_to("0"))
        assert_that(normal_replacements["SKOVERLAY_DISMISSIBLE"], equal_to("default"))
        assert_that(normal_replacements["SKOVERLAY_POSITION"], equal_to("default"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify SKOVERLAY_AUTO='false' when show =0 in bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_02(self, pub_app_id, placement, rtb):

        """
            App level setting
            fullscreenClickable:"fsc_off"

            placement level setting
            fullscreenClickable:"inhert"
           """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {"show": 0}
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', override_bid_ext=json.dumps(override_bid_ext),
                                          rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, "SKOVERLAY_AUTO")

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify jaeger will not serve when no App Store ID and existing skoverlay fields"
                        "in bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_03(self, pub_app_id, placement, rtb):

        override_bid_ext = {
            "skadn": {
                "ext": {
                    "skoverlay": {"show": 1}
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', override_bid_ext=json.dumps(override_bid_ext),
                                          rtb_selector=rtb))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify jaeger will not serve when no App Store ID and existing skoverlay fields "
                        "in bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_04(self, pub_app_id, placement, rtb):
        """
         App level setting
         fullscreenClickable:"fsc_off"

         placement level setting
         fullscreenClickable:"inhert"
        """
        override_bid_ext = {
            "skadn": {
                "ext": {
                    "skoverlay": {"show": 0}
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', override_bid_ext=json.dumps(override_bid_ext),
                                          rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, "SKOVERLAY_AUTO")

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify values of token replacements are correct when parse bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('delay', [0, 5, 60])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_05(self, pub_app_id, placement, delay, rtb):
        """
        App level setting
        fullscreenClickable:"fsc_off"

        placement level setting
        fullscreenClickable:"inhert"
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {"show": 1,
                                  "delay": delay
                                  }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, "SKOVERLAY_AUTO")
        assert_that(normal_replacements["SKOVERLAY_DELAY_SECONDS"], equal_to(str(delay)))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description(
        "Verify jaeger will not server when delay > 60 in skoverlay object of bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('delay', [61, 100])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_06(self, pub_app_id, placement, delay, rtb):

        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {"show": 1,
                                  "delay": delay
                                  }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify jaeger will not server when autoclose is invalid in skoverlay object of "
                        "bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('autoclose', [1, 2, 3, 4, 61])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_07(self, pub_app_id, placement, autoclose, rtb):

        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {"show": 1,
                                  "autoclose": autoclose
                                  }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify token replacement are correct  when autoclose is valid in skoverlay object of"
                        " bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('autoclose', [0, 5, 60])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_08(self, pub_app_id, placement, autoclose, rtb):

        """
         App level setting
         fullscreenClickable:"fsc_off"

         placement level setting
         fullscreenClickable:"inhert"
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {"show": 1,
                                  "autoclose": autoclose
                                  }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, "SKOVERLAY_AUTO")
        assert_that(normal_replacements["SKOVERLAY_AUTO_CLOSE"], equal_to(str(autoclose)))
        assert_that(normal_replacements["SKOVERLAY_DISMISSIBLE"], equal_to("default"))
        assert_that(normal_replacements["SKOVERLAY_POSITION"], equal_to("default"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify token replacement are correct when dismissible is valid in skoverlay object of "
                        "bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('dismissible', [0, 1])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_09(self, pub_app_id, placement, dismissible, rtb):
        """
            App level setting
            fullscreenClickable:"fsc_off"

            placement level setting
            fullscreenClickable:"inhert"
           """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {"show": 1,
                                  "dismissible": dismissible
                                  }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, "SKOVERLAY_AUTO")
        if dismissible == 0:
            assert_that(normal_replacements["SKOVERLAY_DISMISSIBLE"], equal_to("false"))
        elif dismissible == 1:
            assert_that(normal_replacements["SKOVERLAY_DISMISSIBLE"], equal_to("true"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify token replacement are correct when pos is valid in skoverlay object of"
                        " bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('pos', [0, 1])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_10(self, pub_app_id, placement, pos, rtb):
        """
            App level setting
            fullscreenClickable:"fsc_off"

            placement level setting
            fullscreenClickable:"inhert"
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {"show": 1,
                                  "pos": pos
                                  }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, "SKOVERLAY_AUTO")
        if pos == 0:
            assert_that(normal_replacements["SKOVERLAY_POSITION"], equal_to("bottom"))
        elif pos == 1:
            assert_that(normal_replacements["SKOVERLAY_POSITION"], equal_to("bottom-raised"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify token replacement are correct when pos is valid in skoverlay object of"
                        " bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50223'])
    @pytest.mark.parametrize('pos', [0, 1])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_10_1(self, pub_app_id, placement, pos, rtb):
        """
            App level setting
            fullscreenClickable:"fsc_off"

            placement level setting
            fullscreenClickable:"adv_pref"
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {"show": 1,
                                  "click_on_view": 0,
                                  "pos": pos
                                  }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "SKOVERLAY_AUTO")
        assert_that(normal_replacements['SKOVERLAY_AUTO'], equal_to("true"))
        if pos == 0:
            assert_that(normal_replacements["SKOVERLAY_POSITION"], equal_to("bottom"))
        elif pos == 1:
            assert_that(normal_replacements["SKOVERLAY_POSITION"], equal_to("bottom-raised"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify jaeger will not server when show is 0 and other attributes"
                        "are vailid in skoverlay object of bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_11(self, pub_app_id, placement, rtb):

        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {"show": 0,
                                  "delay": 0,
                                  "autoclose": 5,
                                  "dismissible": 1,
                                  "pos": 1
                                  }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify jaeger will not server when no show field but other attributes"
                        "are vailid in skoverlay object of bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_12(self, pub_app_id, placement, rtb):

        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {
                        "delay": 0,
                        "autoclose": 5,
                        "dismissible": 1,
                        "pos": 1
                    }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify jaeger will not server when no app store id but other attributes are valid"
                        "in skoverlay object of bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_13(self, pub_app_id, placement, rtb):

        override_bid_ext = {
            "skadn": {

                "ext": {
                    "skoverlay": {"show": 1,
                                  "delay": 0,
                                  "autoclose": 5,
                                  "dismissible": 1,
                                  "pos": 1
                                  }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify the value of token replacements when for empty skproduct node"
                        "in bid response via lift off")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['AREYOUS82694'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_14(self, pub_app_id, placement, rtb):
        override_bid_ext = {
            "skadn": {
                "ext": {
                    "skproduct": {}
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        # below are checking default value
        assert_that(normal_replacements["SK_FSC"], equal_to("false"))
        assert_that(normal_replacements["SK_FSC"], equal_to("false"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description(
        "Verify token replacement will follow app level setting not in skproduct object of bid response")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('fsc', [1, 0])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_15(self, pub_app_id, placement, fsc, rtb):
        """
        App level setting:

        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "product_view",
            "asoi_complete": "overlay_view",
            "cta_only": "off"
        }
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "123456789",
                "ext": {
                    "skproduct": {
                        "fsc": fsc,
                    }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_that(normal_replacements["SK_FSC"], equal_to("default"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify token replacement will follow skproduct object of bid response "
                        "when no setting in app level")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['DEFAULT02024'])
    @pytest.mark.parametrize('fsc', [1, 0])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_16(self, pub_app_id, placement, fsc, rtb):
        """
        App level setting:

        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "product_view",
            "asoi_complete": "overlay_view",
            "cta_only": "off"
        }
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "123456789",
                "ext": {
                    "skproduct": {
                        "fsc": fsc,
                    }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        if fsc == 0:
            assert_that(normal_replacements["SK_FSC"], equal_to("false"))
        elif fsc == 1:
            assert_that(normal_replacements["SK_FSC"], equal_to("true"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify the value of token replacement"
                        "when end field existing in bid response")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['DEFAULT02024'])
    @pytest.mark.parametrize('end', [1, 0])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_17(self, pub_app_id, placement, end, rtb):
        """
        App level setting:

        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "product_view",
            "asoi_complete": "overlay_view",
            "cta_only": "off"
        }
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "123456789",
                "ext": {
                    "skproduct": {
                        "end": end,
                    }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        if end == 0:
            assert_that(normal_replacements["SK_ENDCARD"], equal_to("false"))
        elif end == 1:
            assert_that(normal_replacements["SK_ENDCARD"], equal_to("true"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify jaeger will not server "
                        "when no app store id but others field of skproduct object existing in bid response")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['DEFAULT02024'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_18(self, pub_app_id, placement, rtb):
        """
        App level setting:

        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "product_view",
            "asoi_complete": "overlay_view",
            "cta_only": "off"
        }
        """
        override_bid_ext = {
            "skadn": {
                "ext": {
                    "skproduct": {
                        "end": 1,
                        "fsc": 1

                    }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify the value of token replacements when skoverylay and skproduct object both existing "
                        " in bid response")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['DEFAULT02024'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_19(self, pub_app_id, placement, rtb):
        """
        App level setting:

        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "product_view",
            "asoi_complete": "overlay_view",
            "cta_only": "off"
        }
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "123456789",
                "ext": {
                    "skoverlay": {"show": 1,
                                  "delay": 0,
                                  "autoclose": 5,
                                  "dismissible": 1,
                                  "pos": 1
                                  },
                    "skproduct": {
                        "end": 1,
                        "fsc": 1

                    }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_that(normal_replacements["SKOVERLAY_DELAY_SECONDS"], equal_to("0"))
        assert_that(normal_replacements["SKOVERLAY_AUTO_CLOSE"], equal_to("5"))
        assert_that(normal_replacements["SKOVERLAY_DISMISSIBLE"], equal_to("true"))
        assert_that(normal_replacements["SKOVERLAY_POSITION"], equal_to("bottom-raised"))
        assert_that(normal_replacements["SK_FSC"], equal_to("true"))
        assert_that(normal_replacements["SK_ENDCARD"], equal_to("true"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3732 Allow StoreKit controls in bid requests from Liftoff eDSP')
    @allure.description("Verify jaeger will not server when no app store id but skoverylay and "
                        "skproduct object  existing in bid response")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['DEFAULT02024'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_token_replacement_parse_from_bid_response_for_liftoff_20(self, pub_app_id, placement, rtb):
        """
        App level setting:

        "storekit": {
            "fsc": "default",
            "asoi_aggressive": "product_view",
            "asoi_complete": "overlay_view",
            "cta_only": "off"
        }
        """
        override_bid_ext = {
            "skadn": {
                "ext": {
                    "skoverlay": {"show": 1,
                                  "delay": 0,
                                  "autoclose": 5,
                                  "dismissible": 1,
                                  "pos": 1
                                  },
                    "skproduct": {
                        "end": 1,
                        "fsc": 1

                    }
                }
            }
        }
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                                                        override_bid_ext=json.dumps(override_bid_ext),
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'v1.236.0')
    @allure.story(
        'PBJ-4582 [Programmatic]Allow DSP partners to override MMP auto-clicks when showing SKOverlay automatically'
        'PBJ-4839 Allow Moloco to override "MMP autoclick" when using SKO Auto'
        'PBJ-4837 Allow DSP partners to opt-in / opt-out "Firing click_on_view for the endcard"')
    @allure.description("Verify enable click_on_view, which allows Vungle to fire MMP auto click")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50223'])
    @pytest.mark.parametrize('rtb', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_allow_fire_mmp_auto_click_setting_true_01(self, pub_app_id, placement, rtb):
        """
        App level setting
        fullscreenClickable:"fsc_off"

        placement level setting
        fullscreenClickable:"adv_pref"

        rtb level setting: "allow_sko_autoclick_override_video":true
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {
                        "show": 1,
                        "click_on_view": 1
                    }
                }
            }
        }

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', rtb_selector=rtb,
                                          override_bid_ext=json.dumps(override_bid_ext)))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "SKOVERLAY_DISABLE_AUTO_MMP")
        assert_that(normal_replacements["SKOVERLAY_DISABLE_AUTO_MMP"], equal_to("false"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'v1.236.0')
    @allure.story(
        'PBJ-4582 [Programmatic]Allow DSP partners to override MMP auto-clicks when showing SKOverlay automatically'
        'PBJ-4839 Allow Moloco to override "MMP autoclick" when using SKO Auto'
        'PBJ-4837 Allow DSP partners to opt-in / opt-out "Firing click_on_view for the endcard')
    @allure.description("Verify disable click_on_view, which dont allow Vungle to fire MMP auto click")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50223'])
    @pytest.mark.parametrize('rtb', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_allow_fire_mmp_auto_click_setting_true_02(self, pub_app_id, placement, rtb):
        """
        App level setting
        fullscreenClickable:"fsc_off"

        placement level setting
        fullscreenClickable:"adv_pref"

        rtb level setting: "allow_sko_autoclick_override_video":true
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {
                        "show": 1,
                        "click_on_view": 0
                    }
                }
            }
        }

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', override_bid_ext=json.dumps(override_bid_ext),
                                          rtb_selector=rtb))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "SKOVERLAY_DISABLE_AUTO_MMP")
        assert_that(normal_replacements["SKOVERLAY_DISABLE_AUTO_MMP"], equal_to("true"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'v1.236.0')
    @allure.story(
        'PBJ-4582 [Programmatic]Allow DSP partners to override MMP auto-clicks when showing SKOverlay automatically'
        'PBJ-4839 Allow Moloco to override "MMP autoclick" when using SKO Auto'
        'PBJ-4837 Allow DSP partners to opt-in / opt-out "Firing click_on_view for the endcard')
    @allure.description("Verify click_on_view is none, which dont Vungle to fire MMP auto click")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50223'])
    @pytest.mark.parametrize('rtb', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_allow_fire_mmp_auto_click_setting_true_03(self, pub_app_id, placement, rtb):
        """
        App level setting
        fullscreenClickable:"fsc_off"

        placement level setting
        fullscreenClickable:"adv_pref"

        rtb level setting: "allow_sko_autoclick_override_video":true
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {
                        "show": 1,
                        "click_on_view": None
                    }
                }
            }
        }

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', rtb_selector=rtb,
                                          override_bid_ext=json.dumps(override_bid_ext)))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "SKOVERLAY_DISABLE_AUTO_MMP")
        assert_that(normal_replacements["SKOVERLAY_DISABLE_AUTO_MMP"], equal_to("false"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'v1.236.0')
    @allure.story(
        'PBJ-4582 [Programmatic]Allow DSP partners to override MMP auto-clicks when showing SKOverlay automatically'
        'PBJ-4837 Allow DSP partners to opt-in / opt-out "Firing click_on_view for the endcard')
    @allure.description("Verify rtb flag is false/no setting will not override the value of the token")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50223'])
    @pytest.mark.parametrize('rtb',
                             [ext_non_test_mode_kraken_rtb_ids_vast_moloco, ext_non_test_mode_kraken_rtb_ids_vast])
    def test_default_allow_fire_mmp_auto_click_setting_false_01(self, pub_app_id, placement, rtb):
        """
          App level setting
          fullscreenClickable:"fsc_off"

          placement level setting
          fullscreenClickable:"adv_pref"

          rtb level setting: "allow_sko_autoclick_override_video":false
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {
                        "show": 1,
                        "click_on_view": 1
                    }
                }
            }
        }

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', rtb_selector=rtb,
                                          override_bid_ext=json.dumps(override_bid_ext)))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "SKOVERLAY_DISABLE_AUTO_MMP")
        assert_that(normal_replacements["SKOVERLAY_DISABLE_AUTO_MMP"], equal_to("false"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'v1.236.0')
    @allure.story(
        'PBJ-4582 [Programmatic]Allow DSP partners to override MMP auto-clicks when showing SKOverlay automatically'
        'PBJ-4837 Allow DSP partners to opt-in / opt-out "Firing click_on_view for the endcard')
    @allure.description("Verify rtb flag is false/no setting will not override the value of the token")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50223'])
    @pytest.mark.parametrize('rtb',
                             [ext_non_test_mode_kraken_rtb_ids_vast_moloco, ext_non_test_mode_kraken_rtb_ids_vast])
    def test_default_allow_fire_mmp_auto_click_setting_false_02(self, pub_app_id, placement, rtb):
        """
          App level setting
          fullscreenClickable:"fsc_off"

          placement level setting
          fullscreenClickable:"adv_pref"

          rtb level setting: "allow_sko_autoclick_override_video":false
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {
                        "show": 1,
                        "click_on_view": 0
                    }
                }
            }
        }

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', rtb_selector=rtb,
                                          override_bid_ext=json.dumps(override_bid_ext)))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "SKOVERLAY_DISABLE_AUTO_MMP")
        assert_that(normal_replacements["SKOVERLAY_DISABLE_AUTO_MMP"], equal_to("false"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format', 'v1.236.0')
    @allure.story(
        'PBJ-4582 [Programmatic]Allow DSP partners to override MMP auto-clicks when showing SKOverlay automatically'
        'PBJ-4837 Allow DSP partners to opt-in / opt-out "Firing click_on_view for the endcard')
    @allure.description("Verify rtb flag is false/no setting will not override the value of the token")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50223'])
    @pytest.mark.parametrize('rtb',
                             [ext_non_test_mode_kraken_rtb_ids_vast_moloco, ext_non_test_mode_kraken_rtb_ids_vast])
    def test_default_allow_fire_mmp_auto_click_setting_false_02(self, pub_app_id, placement, rtb):
        """
          App level setting
          fullscreenClickable:"fsc_off"

          placement level setting
          fullscreenClickable:"adv_pref"

          rtb level setting: "allow_sko_autoclick_override_video":false
        """
        override_bid_ext = {
            "skadn": {
                "itunesitem": "234567890",
                "ext": {
                    "skoverlay": {
                        "show": 1,
                        "click_on_view": None
                    }
                }
            }
        }

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', rtb_selector=rtb,
                                          override_bid_ext=json.dumps(override_bid_ext)))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "SKOVERLAY_DISABLE_AUTO_MMP")
        assert_that(normal_replacements["SKOVERLAY_DISABLE_AUTO_MMP"], equal_to("false"))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3366 Support SKoverlay control for the iOS apps on app and placement level')
    @allure.description("Test template token value for there is fullScreenClickable setting in app level and "
                        "fullScreenClickable =fsc_on in placement level")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_skoverlay_config_placement_level_setting_01(self, pub_app_id, placement, rtb):
        """
        App level setting
        fullscreenClickable:fsc_off

        placement level setting
        fullscreenClickable: fsc_on
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(normal_replacements, 'FULL_CTA_OPTION')
        assert_that(normal_replacements['FULL_CTA_OPTION'], 'fsc_on')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3366 Support SKoverlay control for the iOS apps on app and placement level')
    @allure.description("Test template token value for there is fullScreenClickable setting in app level and "
                        "in placement level")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['6124c3ec656f515cfe3050b3'])
    @pytest.mark.parametrize('placement', ['No_FSC'])
    def test_skoverlay_previous_setting_for_app_and_placemeny_level_config(self, pub_app_id, placement):
        """
        App level setting
        clickableVideoEnabled: false

        placement level setting
        clickableVideoEnabled: true
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(normal_replacements, 'FULL_CTA')
        assert_that(normal_replacements['FULL_CTA'], equal_to('true'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3366 Support SKoverlay control for the iOS apps on app and placement level')
    @allure.description("Test template token value for there is  ullScreenClickable setting in app level and "
                        "empty in placement level")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['6124c3ec656f515cfe3050b3'])
    @pytest.mark.parametrize('placement', ['No_FSC_NO_CLK'])
    def test_skoverlay_previous_setting_for_app_and_empty_placement(self, pub_app_id, placement):
        """
        App level setting
        clickableVideoEnabled: false

        placement level setting
        clickableVideoEnabled: empty
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(normal_replacements, 'FULL_CTA')
        assert_that(normal_replacements['FULL_CTA'], equal_to('false'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3366 Support SKoverlay control for the iOS apps on app and placement level')
    @allure.description("Test template token value for android platform")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', ['DEFAULT95027'])
    def test_skoverlay_config_setting_for_android(self, pub_app_id, placement):
        """
        App level setting
        clickableVideoEnabled: false

        placement level setting
        clickableVideoEnabled: true
        """
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        if 'templateSettings' in response_payload['ads'][0]['ad_markup']:
            normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_keys_exist(normal_replacements, 'FULL_CTA')
            assert_that(normal_replacements['FULL_CTA'], equal_to('true'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3366 Support SKoverlay control for the iOS apps on app and placement level')
    @allure.description("Test template token value for android platform")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', ['DEFAULT95028'])
    def test_skoverlay_config_setting_empty_placement_for_android(self, pub_app_id, placement):
        """
        App level setting
        clickableVideoEnabled: false

        placement level setting
        empty
        """
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=jp_ip, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(normal_replacements, 'FULL_CTA')
        assert_that(normal_replacements['FULL_CTA'], equal_to('false'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3366 Support SKoverlay control for the iOS apps on app and placement level')
    @allure.description("Test template token value for windows platform")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', ['REWARDEDDT-0648490'])
    def test_skoverlay_config_setting_for_windows(self, pub_app_id, placement):
        """
        App level setting
        clickableVideoEnabled: false

        placement level setting
        clickableVideoEnabled: true
        """
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(normal_replacements, 'FULL_CTA')
        assert_that(normal_replacements['FULL_CTA'], equal_to('true'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3366 Support SKoverlay control for the iOS apps on app and placement level')
    @allure.description("Test template token value for windows platform")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', ['REWARDEDDT-0648491'])
    def test_skoverlay_config_setting_for_empty_placement_windows(self, pub_app_id, placement):
        """
        App level setting
        clickableVideoEnabled: false

        placement level setting
        empty
        """
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(normal_replacements, 'FULL_CTA')
        assert_that(normal_replacements['FULL_CTA'], equal_to('false'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description("Test template token value for there is fullScreenClickable setting in app level and "
                        "fullScreenClickable=fsc_on in placement level for eDSP")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_skoverlay_config_placement_level_setting_01e(self, pub_app_id, placement, rtb):
        """
        App level setting
        fullscreenClickable:fsc_off

        placement level setting
        fullscreenClickable: fsc_on
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(normal_replacements, 'FULL_CTA_OPTION')
        assert_that(normal_replacements['FULL_CTA_OPTION'], 'fsc_on')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description("Test template token value for there is  ullScreenClickable setting in app level and "
                        "in placement level for eDSP")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['6124c3ec656f515cfe3050b3'])
    @pytest.mark.parametrize('placement', ['No_FSC'])
    def test_skoverlay_previous_setting_for_app_and_placemeny_level_config_e(self, pub_app_id, placement):
        """
        App level setting
        clickableVideoEnabled: false

        placement level setting
        clickableVideoEnabled: true
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(normal_replacements, 'FULL_CTA')
        assert_that(normal_replacements['FULL_CTA'], equal_to('true'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description("Test template token value for there is  ullScreenClickable setting in app level and "
                        "empty in placement level for eDSP")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['6124c3ec656f515cfe3050b3'])
    @pytest.mark.parametrize('placement', ['No_FSC_NO_CLK'])
    def test_skoverlay_previous_setting_for_app_and_empty_placement_e(self, pub_app_id, placement):
        """
        App level setting
        clickableVideoEnabled: false

        placement level setting
        clickableVideoEnabled: empty
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(normal_replacements, 'FULL_CTA')
        assert_that(normal_replacements['FULL_CTA'], equal_to('false'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description("Test template token value for android platform for eDSP")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', ['DEFAULT95027'])
    def test_skoverlay_config_setting_for_android_e(self, pub_app_id, placement):
        """
        App level setting
        clickableVideoEnabled: false

        placement level setting
        clickableVideoEnabled: true
        """
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        if 'templateSettings' in response_payload['ads'][0]['ad_markup']:
            normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_keys_exist(normal_replacements, 'FULL_CTA')
            assert_that(normal_replacements['FULL_CTA'], equal_to('true'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description("Test template token value for android platform for eDSP")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', ['DEFAULT95028'])
    def test_skoverlay_config_setting_empty_placement_for_android_e(self, pub_app_id, placement):
        """
        App level setting
        clickableVideoEnabled: false

        placement level setting
        empty
        """
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=jp_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(normal_replacements, 'FULL_CTA')
        assert_that(normal_replacements['FULL_CTA'], equal_to('false'))

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3944 SKO auto show flag should reflect publisher settings')
    @allure.description(
        "Verify the value of 'FULL_CTA_OPTION' token when pub setting 'adv_pref' and placement setting inhert")
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('placement', ['COPPA-TEST_01'])
    @pytest.mark.parametrize('rtb_ids', [meister_rtb_ids, ext1_non_test_mode_kraken_rtb_ids_mraid])
    def test_sko_auto_show_flag_01(self, pub_app_id, placement, rtb_ids):
        """
        App level setting
        fullscreenClickable:"adv_pref"

        placement level setting
        fullscreenClickable:"inhert"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=jp_ip, rtb_selector=rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(normal_replacements, 'FULL_CTA_OPTION')
        assert_that(normal_replacements['FULL_CTA_OPTION'], 'adv_pref')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3944 SKO auto show flag should reflect publisher settings')
    @allure.description("Verify the value of 'FULL_CTA_OPTION' token when pub setting 'adv_pref' "
                        "and placement setting 'adv_pref'")
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('placement', ['COPPA-TEST_02'])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_mraid])
    def test_sko_auto_show_flag_01_1(self, pub_app_id, placement, rtb_ids):
        """
        App level setting
        fullscreenClickable:"adv_pref"

        placement level setting
        fullscreenClickable:"adv_pref"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=jp_ip, rtb_selector=rtb_ids))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(normal_replacements, 'FULL_CTA_OPTION')
        assert_that(normal_replacements['FULL_CTA_OPTION'], 'adv_pref')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3944 SKO auto show flag should reflect publisher settings')
    @allure.description("Verify the value of 'FULL_CTA_OPTION' token when pub setting adv_pref "
                        "and placement setting fsc_off")
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('placement', ['DEFAULT-5045327'])
    @pytest.mark.parametrize('rtb_ids', [non_test_mode_kraken_rtb_ids, ext1_non_test_mode_kraken_rtb_ids_mraid])
    def test_sko_auto_show_flag_02(self, pub_app_id, placement, rtb_ids):
        """
        App level setting
        fullscreenClickable:"adv_pref"

        placement level setting
        fullscreenClickable:"fsc_off"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids, debug='jaeger'))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(normal_replacements, 'FULL_CTA_OPTION')
        assert_that(normal_replacements['FULL_CTA_OPTION'], 'fsc_off')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3944 SKO auto show flag should reflect publisher settings')
    @allure.description("Verify the value of 'FULL_CTA_OPTION' token when pub setting"
                        " fsc_off and placement setting adv_pref")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50223'])
    def test_sko_auto_show_flag_03(self, pub_app_id, placement):
        """
        App level setting
        fullscreenClickable:"fsc_off"

        placement level setting
        fullscreenClickable:"adv_pref"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=jp_ip, rtb_selector=ext1_non_test_mode_kraken_rtb_ids_mraid))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(normal_replacements, 'FULL_CTA_OPTION')
        assert_that(normal_replacements['FULL_CTA_OPTION'], 'adv_pref')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3944 SKO auto show flag should reflect publisher settings')
    @allure.description("Verify the value of 'FULL_CTA_OPTION' token "
                        "when pub setting fsc_off and placement setting inherit")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_sko_auto_show_flag_04(self, pub_app_id, placement):
        """
        App level setting
        fullscreenClickable:"fsc_off"

        placement level setting
        fullscreenClickable:"inherit"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=jp_ip, rtb_selector=ext1_non_test_mode_kraken_rtb_ids_mraid))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(normal_replacements, 'FULL_CTA_OPTION')
        assert_that(normal_replacements['FULL_CTA_OPTION'], 'fsc_off')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3944 SKO auto show flag should reflect publisher settings')
    @allure.description("Verify the value of 'FULL_CTA_OPTION' token "
                        "when pub setting fsc_off and placement setting fsc_on")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    def test_sko_auto_show_flag_05(self, pub_app_id, placement):
        """
        App level setting
        fullscreenClickable:"fsc_off"

        placement level setting
        fullscreenClickable:"fsc_on"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=jp_ip, rtb_selector=ext1_non_test_mode_kraken_rtb_ids_mraid))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'FULL_CTA_OPTION')
        assert_that(normal_replacements['FULL_CTA_OPTION'], 'fsc_on')

    @allure.feature('skoverlay')
    @allure.tag('normal', 'ad_format')
    @allure.story('PBJ-3944 SKO auto show flag should reflect publisher settings')
    @allure.description("Verify the value of 'FULL_CTA_OPTION' token "
                        "when pub setting fsc_off and placement setting fsc_off")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50203'])
    def test_sko_auto_show_flag_06(self, pub_app_id, placement):
        """
        App level setting
        fullscreenClickable:"fsc_off"

        placement level setting
        fullscreenClickable:"fsc_off"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=jp_ip, rtb_selector=ext1_non_test_mode_kraken_rtb_ids_mraid))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(normal_replacements, 'FULL_CTA_OPTION')
        assert_that(normal_replacements['FULL_CTA_OPTION'], 'fsc_off')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2689 Macro substitutions in view tracking')
    @allure.description('Verify the macros in viewability data can be populated correctly for ios in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_macro_viewability_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        omsdk_data = base64.b64decode(normal_replacements['OM_SDK_DATA'].encode('ascii')).decode('ascii')

        assert_that(str_to_json(ad_markup['app_id'].replace('$0$', ''))['app_id'] in omsdk_data)
        assert_that(ad_markup['campaign'].split('|')[0] in omsdk_data)
        assert_that(ad_markup['campaign'].split('|')[1] in omsdk_data)
        assert_that(placement in omsdk_data)
        assert_that(pub_app_id in omsdk_data)
        if env == 'ci':
            assert_that(ext_test_mode_kraken_rtb_ids_vast.split(',')[0] in omsdk_data)
        elif env == 'qa' or env == 'regression':
            assert_that(ext_test_mode_kraken_rtb_ids_vast.split(',')[1] in omsdk_data)

    @allure.feature('omsdk support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2689 Macro substitutions in view tracking')
    @allure.description('Verify the macros in viewability data can be populated correctly for ios')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_macro_viewability_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        omsdk_data = base64.b64decode(normal_replacements['OM_SDK_DATA'].encode('ascii')).decode('ascii')

        assert_that(str_to_json(ad_markup['app_id'].replace('$0$', ''))['app_id'] in omsdk_data)
        assert_that(ad_markup['campaign'].split('|')[0] in omsdk_data)
        assert_that(ad_markup['campaign'].split('|')[1] in omsdk_data)
        assert_that(placement in omsdk_data)
        assert_that(pub_app_id in omsdk_data)
        if env == 'ci':
            assert_that(ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0] in omsdk_data)
        elif env == 'qa' or env == 'regression':
            assert_that(ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1] in omsdk_data)

    @allure.feature('omsdk support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2689 Macro substitutions in view tracking')
    @allure.description('Verify the macros in viewability data can be populated correctly for android in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_macro_viewability_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        omsdk_data = base64.b64decode(normal_replacements['OM_SDK_DATA'].encode('ascii')).decode('ascii')

        assert_that(str_to_json(ad_markup['app_id'].replace('$0$', ''))['app_id'] in omsdk_data)
        assert_that(ad_markup['campaign'].split('|')[0] in omsdk_data)
        assert_that(ad_markup['campaign'].split('|')[1] in omsdk_data)
        assert_that(placement in omsdk_data)
        assert_that(pub_app_id in omsdk_data)
        if env == 'ci':
            assert_that(ext_test_mode_kraken_rtb_ids_vast.split(',')[0] in omsdk_data)
        elif env == 'qa' or env == 'regression':
            assert_that(ext_test_mode_kraken_rtb_ids_vast.split(',')[1] in omsdk_data)

    @allure.feature('omsdk support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2689 Macro substitutions in view tracking')
    @allure.description('Verify the macros in viewability data can be populated correctly for android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_macro_viewability_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        omsdk_data = base64.b64decode(normal_replacements['OM_SDK_DATA'].encode('ascii')).decode('ascii')

        assert_that(str_to_json(ad_markup['app_id'].replace('$0$', ''))['app_id'] in omsdk_data)
        assert_that(ad_markup['campaign'].split('|')[0] in omsdk_data)
        assert_that(ad_markup['campaign'].split('|')[1] in omsdk_data)
        assert_that(placement in omsdk_data)
        assert_that(pub_app_id in omsdk_data)
        if env == 'ci':
            assert_that(ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0] in omsdk_data)
        elif env == 'qa' or env == 'regression':
            assert_that(ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1] in omsdk_data)

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.170.0')
    @allure.story('PBJ-3038 storeID information in Programmatic banner/Mrec Ads')
    @allure.description('Verify ad markup ad_market_id from ads response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_fields_programmatic_banner(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_that(normal_replacements['APP_STORE_ID'], equal_to(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle']))
        assert_that('https://apps.apple.com/app/id' in normal_replacements['CTA_BUTTON_URL'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.170.0', 'test_mode')
    @allure.story('PBJ-3038 storeID information in Programmatic banner/Mrec Ads')
    @allure.description('Verify ad markup ad_market_id from ads response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_fields_programmatic_banner_test_mode(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_that(normal_replacements['APP_STORE_ID'], equal_to(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle']))
        assert_that('https://apps.apple.com/app/id' in normal_replacements['CTA_BUTTON_URL'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.170.0')
    @allure.story('PBJ-3038 storeID information in Programmatic banner/Mrec Ads')
    @allure.description('Verify ad markup ad_market_id from ads response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    def test_fields_programmatic_mrec(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_that(normal_replacements['APP_STORE_ID'], equal_to(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle']))
        assert_that('https://apps.apple.com/app/id' in normal_replacements['CTA_BUTTON_URL'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.170.0', 'test_mode')
    @allure.story('PBJ-3038 storeID information in Programmatic banner/Mrec Ads')
    @allure.description('Verify ad markup ad_market_id from ads response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    def test_fields_programmatic_mrec_test_mode(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_that(normal_replacements['APP_STORE_ID'], equal_to(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle']))
        assert_that('https://apps.apple.com/app/id' in normal_replacements['CTA_BUTTON_URL'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4038 Add \'VUNGLE_PRIVACY_URL\' token in ads response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    def test_pricy_token_programmatic_mrec_test_mode(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'VUNGLE_PRIVACY_URL')
        assert_that(normal_replacements['VUNGLE_PRIVACY_URL'], equal_to('https://privacy.liftoff.io/'))

    @allure.feature('programmatic support')
    @allure.tag('normal')
    @allure.story('PBJ-4038 Add \'VUNGLE_PRIVACY_URL\' token in ads response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_pricy_token_programmatic_banner(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext1_non_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'VUNGLE_PRIVACY_URL')
        assert_that(normal_replacements['VUNGLE_PRIVACY_URL'], equal_to('https://privacy.liftoff.io/'))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0', 'v1.172.0')
    @allure.story('PBJ-3037 bid response for native placement, PBJ-3075 Ads response for native ads')
    @allure.description('Verify the normal replacements info for native type placement via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_normal_replacements_native_placement_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=us_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_that('APP_NAME' in normal_replacements)
        assert_that('APP_DESCRIPTION' in normal_replacements)
        assert_that('SPONSORED_BY' in normal_replacements)
        assert_that('APP_RATING_VALUE' in normal_replacements)
        assert_that('CTA_BUTTON_URL' in normal_replacements)
        assert_that('CTA_BUTTON_TEXT' in normal_replacements)

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0', 'v1.172.0', 'test_mode')
    @allure.story('PBJ-3037 bid response for native placement, PBJ-3075 Ads response for native ads')
    @allure.description('Verify the normal replacements info for native type placement via iDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_normal_replacements_native_placement_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=test_default_real_time_sdk_version,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_that('APP_NAME' in normal_replacements)
        assert_that('APP_DESCRIPTION' in normal_replacements)
        assert_that('SPONSORED_BY' in normal_replacements)
        assert_that('APP_RATING_VALUE' in normal_replacements)
        assert_that('CTA_BUTTON_URL' in normal_replacements)
        assert_that('CTA_BUTTON_TEXT' in normal_replacements)

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0', 'v1.172.0')
    @allure.story('PBJ-3037 bid response for native placement, PBJ-3075 Ads response for native ads')
    @allure.description('Verify the normal replacements info for native type placement via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_normal_replacements_native_placement_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast, debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_that('APP_NAME' in normal_replacements)
        assert_that('APP_DESCRIPTION' in normal_replacements)
        assert_that('SPONSORED_BY' in normal_replacements)
        assert_that('APP_RATING_VALUE' in normal_replacements)
        assert_that('CTA_BUTTON_URL' in normal_replacements)
        assert_that('CTA_BUTTON_TEXT' in normal_replacements)

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0', 'v1.172.0', 'test_mode')
    @allure.story('PBJ-3037 bid response for native placement, PBJ-3075 Ads response for native ads')
    @allure.description('Verify the normal replacements info for native type placement via eDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_normal_replacements_native_placement_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_that('APP_NAME' in normal_replacements)
        assert_that('APP_DESCRIPTION' in normal_replacements)
        assert_that('SPONSORED_BY' in normal_replacements)
        assert_that('APP_RATING_VALUE' in normal_replacements)
        assert_that('CTA_BUTTON_URL' in normal_replacements)
        assert_that('CTA_BUTTON_TEXT' in normal_replacements)

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3333 Cannot fill AdMarketID from SKAdNetwork information')
    @allure.description('Verify the store id will be filled by itunesitem from skadn if no bundle in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_store_id_fill_fix_1(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = ext2_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                              override_bid_response_any='seatbid.0.bid.0.bundle@\"\"'))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            ad_market_id = bid_response[rtb]['seatbid'][0]['bid'][0]['ext']['skadn']['itunesitem']
            assert_that(normal_replacements['APP_STORE_ID'], equal_to(ad_market_id))
            assert_that(normal_replacements['CTA_BUTTON_URL'], equal_to('https://apps.apple.com/app/id' + ad_market_id))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3333 Cannot fill AdMarketID from SKAdNetwork information')
    @allure.description('Verify the store id will be filled by itunesitem from skadn if no bundle in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    def test_store_id_fill_fix_2(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = ext2_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                              override_bid_response_any='seatbid.0.bid.0.bundle@\"\"'))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            ad_market_id = bid_response[rtb]['seatbid'][0]['bid'][0]['ext']['skadn']['itunesitem']
            assert_that(normal_replacements['APP_STORE_ID'], equal_to(ad_market_id))
            assert_that(normal_replacements['CTA_BUTTON_URL'], equal_to('https://apps.apple.com/app/id' + ad_market_id))

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0')
    @allure.story('PBJ-3304 RTB :: Faulty Clicks and No Ad')
    @allure.description('Verify end card cta url can handle the enter and tab symbol for VAST adm')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_cta_url_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_that(normal_replacements['EC_CTA_URL'].find("\t"), equal_to(-1))
        assert_that(normal_replacements['EC_CTA_URL'].find("\n"), equal_to(-1))

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0', 'test_mode')
    @allure.story('PBJ-3304 RTB :: Faulty Clicks and No Ad')
    @allure.description('Verify end card cta url can handle the enter and tab symbol for VAST adm in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_cta_url_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_that(normal_replacements['EC_CTA_URL'].find("\t"), equal_to(-1))
        assert_that(normal_replacements['EC_CTA_URL'].find("\n"), equal_to(-1))

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0')
    @allure.story('PBJ-3304 RTB :: Faulty Clicks and No Ad')
    @allure.description('Verify cta button url can handle the enter and tab symbol for VAST adm')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_cta_url_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_that(normal_replacements['CTA_BUTTON_URL'].find("\t"), equal_to(-1))
        assert_that(normal_replacements['CTA_BUTTON_URL'].find("\n"), equal_to(-1))

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0', 'test_mode')
    @allure.story('PBJ-3304 RTB :: Faulty Clicks and No Ad')
    @allure.description('Verify cta button url can handle the enter and tab symbol for VAST adm in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_cta_url_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_that(normal_replacements['CTA_BUTTON_URL'].find("\t"), equal_to(-1))
        assert_that(normal_replacements['CTA_BUTTON_URL'].find("\n"), equal_to(-1))

    @allure.feature('omsdk support')
    @allure.tag('normal', 'v1.188.0', 'test_mode')
    @allure.story('PBJ-3488 Serve omsdk enabled ad in prod env for IAB verification')
    @allure.description('Verify the omsdk test ad will be returned by Kraken if omid flag is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_omsdk_test_support_1(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_int3_rtb_ids, omid='true'))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
            assert_keys_exist(normal_replacements, 'OM_SDK_DATA')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'v1.188.0', 'test_mode')
    @allure.story('PBJ-3488 Serve omsdk enabled ad in prod env for IAB verification')
    @allure.description('Verify the omsdk test ad will not be returned by Kraken if omid flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_omsdk_test_support_2(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_int3_rtb_ids, omid='false',
                                              debug='jaeger'))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
            assert_keys_not_exist(normal_replacements, 'OM_SDK_DATA')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'v1.188.0', 'test_mode')
    @allure.story('PBJ-3488 Serve omsdk enabled ad in prod env for IAB verification')
    @allure.description('Verify the omsdk test ad will not be returned by Kraken if omid flag is not exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_omsdk_test_support_3(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_int3_rtb_ids))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
            assert_keys_not_exist(normal_replacements, 'OM_SDK_DATA')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'v1.188.0', 'test_mode')
    @allure.story('PBJ-3488 Serve omsdk enabled ad in prod env for IAB verification')
    @allure.description('Verify the omsdk test ad will be returned by Kraken if omid flag is true but the Kraken '
                        'pod does not set the related env variable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_omsdk_test_support_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_int4_rtb_ids, omid='true'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'OM_SDK_DATA')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'v1.188.0', 'test_mode')
    @allure.story('PBJ-3488 Serve omsdk enabled ad in prod env for IAB verification')
    @allure.description('Verify the omsdk test flag does not impact eDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_omsdk_test_support_5(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast, omid='false'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'OM_SDK_DATA')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'v1.188.0')
    @allure.story('PBJ-3488 Serve omsdk enabled ad in prod env for IAB verification')
    @allure.description('Verify the omsdk test flag does not impact eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_omsdk_test_support_6(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          omid='false'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'OM_SDK_DATA')

    @allure.feature('rtb')
    @allure.tag('normal', 'v1.190.0', 'v1.190.1', 'v1.219.0')
    @allure.story('PBJ-3585 temperate server side fix for SDK CTA URL encode issue'
                  'PBJ-3625 Server side fix(PBJ-3585) is not working for IOS SDK in some cases'
                  'PBJ-4290 Fix CTA encoding issues for Appier and Moloco.')
    @allure.description('Verify the cta url will not be decoded via the specific eDSP rtb for iOS')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb_id', [ext_test_mode_kraken_rtb_ids_vast_uri_decode, '5f107d3c82cd5a0016476a14'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.4'])
    def test_cta_url_decode_1(self, pub_app_id, placement, rtb_id, sdk_v):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_id, debug='jaeger', sdk_version=sdk_v))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
            assert_that('https%3A%2F%2F' in normal_replacements['CTA_BUTTON_URL'])
            assert_that('https%3A%2F%2F' in normal_replacements['EC_CTA_URL'])

    @allure.feature('rtb')
    @allure.tag('normal', 'v1.190.0', 'v1.190.1')
    @allure.story('PBJ-3585 temperate server side fix for SDK CTA URL encode issue'
                  'PBJ-3625 Server side fix(PBJ-3585) is not working for IOS SDK in some cases')
    @allure.description('Verify the cta url will not be decoded via the rtb not in the specific eDSP list for iOS')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_cta_url_decode_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_that('https%3A%2F%2F' in normal_replacements['CTA_BUTTON_URL'])
        assert_that('https%3A%2F%2F' in normal_replacements['EC_CTA_URL'])

    @allure.feature('rtb')
    @allure.tag('normal', 'v1.190.0', 'v1.190.1', 'test_mode')
    @allure.story('PBJ-3585 temperate server side fix for SDK CTA URL encode issue'
                  'PBJ-3625 Server side fix(PBJ-3585) is not working for IOS SDK in some cases')
    @allure.description('Verify the cta url will not be decoded if the specific rtb in iDSP for iOS')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_cta_url_decode_3(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids_uri_decode))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
            assert_that('https%3A%2F%2F' in normal_replacements['CTA_BUTTON_URL'])

    @allure.feature('rtb')
    @allure.tag('normal', 'v1.190.0', 'v1.190.1', 'test_mode')
    @allure.story('PBJ-3585 temperate server side fix for SDK CTA URL encode issue'
                  'PBJ-3625 Server side fix(PBJ-3585) is not working for IOS SDK in some cases')
    @allure.description('Verify the cta url will not be decoded if the iDPS rtb is not on the specific list for iOS')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_cta_url_decode_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_that('https%3A%2F%2F' in normal_replacements['CTA_BUTTON_URL'])

    @allure.feature('rtb')
    @allure.tag('normal', 'v1.190.0', 'v1.190.1', 'v1.219.0')
    @allure.story('PBJ-3585 temperate server side fix for SDK CTA URL encode issue'
                  'PBJ-3625 Server side fix(PBJ-3585) is not working for IOS SDK in some cases'
                  'PBJ-4290 Fix CTA encoding issues for Appier and Moloco.')
    @allure.description(
        'Verify the cta url can be decoded via the specific eDSP rtb for Android for sdk version < 6.11')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('rtb_id', [ext_test_mode_kraken_rtb_ids_vast_uri_decode, '5f107d3c82cd5a0016476a14'])
    def test_cta_url_decode_5(self, pub_app_id, placement, rtb_id):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_id, sdk_version='Vungle/6.10.4'))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
            assert_that('https%3A%2F%2F' not in normal_replacements['CTA_BUTTON_URL'])
            assert_that('https%3A%2F%2F' not in normal_replacements['EC_CTA_URL'])

    @allure.feature('rtb')
    @allure.tag('normal', 'v1.190.0', 'v1.190.1', 'v1.219.0')
    @allure.story('PBJ-4290 Fix CTA encoding issues for Appier and Moloco.')
    @allure.description(
        'Verify the cta url can not be decoded via the specific eDSP rtb for Android for sdk version>=6.11')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('rtb_id', [ext_test_mode_kraken_rtb_ids_vast_uri_decode, '5f107d3c82cd5a0016476a14'])
    def test_cta_url_decode_5_1(self, pub_app_id, placement, rtb_id):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_id, sdk_version='Vungle/6.11.1'))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
            assert_that('https%3A%2F%2F' in normal_replacements['CTA_BUTTON_URL'])
            assert_that('https%3A%2F%2F' in normal_replacements['EC_CTA_URL'])

    @allure.feature('rtb')
    @allure.tag('normal', 'v1.190.0', 'v1.190.1')
    @allure.story('PBJ-3585 temperate server side fix for SDK CTA URL encode issue'
                  'PBJ-3625 Server side fix(PBJ-3585) is not working for IOS SDK in some cases')
    @allure.description('Verify the cta url will not be decoded via the rtb not in the specific eDSP list for Android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_cta_url_decode_6(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_that('https%3A%2F%2F' in normal_replacements['CTA_BUTTON_URL'])
        assert_that('https%3A%2F%2F' in normal_replacements['EC_CTA_URL'])

    @allure.feature('rtb')
    @allure.tag('normal', 'v1.190.0', 'v1.190.1', 'test_mode')
    @allure.story('PBJ-3585 temperate server side fix for SDK CTA URL encode issue'
                  'PBJ-3625 Server side fix(PBJ-3585) is not working for IOS SDK in some cases')
    @allure.description('Verify the cta url will not be decoded if the specific rtb in iDSP for Android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_cta_url_decode_7(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids_uri_decode))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
            assert_that('https%3A%2F%2F' in normal_replacements['CTA_BUTTON_URL'])

    @allure.feature('rtb')
    @allure.tag('normal', 'v1.190.0', 'v1.190.1', 'test_mode')
    @allure.story('PBJ-3585 temperate server side fix for SDK CTA URL encode issue'
                  'PBJ-3625 Server side fix(PBJ-3585) is not working for IOS SDK in some cases')
    @allure.description('Verify the cta url will not be decoded if the iDPS rtb is not on the specific list '
                        'for Android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_cta_url_decode_8(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids, debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        assert_that('https%3A%2F%2F' in normal_replacements['CTA_BUTTON_URL'])

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode', 'v1.195.0')
    @allure.story('PBJ-3695 Send Vungle Privacy URL for programmaticFullscreen template')
    @allure.description('Verify the vungle privacy url under the normal replacements in test mode')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_vungle_privacy_url_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip,
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_that('VUNGLE_PRIVACY_URL' in normal_replacements)

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'v1.195.0')
    @allure.story('PBJ-3695 Send Vungle Privacy URL for programmaticFullscreen template')
    @allure.description('Verify the vungle privacy url under the normal replacements')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_vungle_privacy_url_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_that('VUNGLE_PRIVACY_URL' in normal_replacements)

    @allure.feature('max latency experiment')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4458 AB testing to identify the Maximum Acceptable Latency between PlayAd and impression')
    @allure.description('Verify that iOS pub app enter the experiment with duration token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_max_latency_exp_1(self, pub_app_id, placement):
        '''
            "templateId": "58c2f62c34f5e387180003fa" from the mocked ad

            {
              "_id": {
                "$oid": "62de2db8bf51a2a06de84975"
              },
              "name": "Max_Latency_Experiment_phase1",
              "mutual_id": "62d4f4ef3571cd891d472cce",
              "allocate_strategy": "math_random",
              "salt": "62de2e2274b41f3c74958e5f",
              "countries": [],
              "is_all_countries": true,
              "is_all_applications": false,
              "traffic_percentage": 10000,
              "scope": "jaeger",
              "start_date": {
                "$date": {
                  "$numberLong": "1551398400000"
                }
              },
              "end_date": {
                "$date": {
                  "$numberLong": "4102444799999"
                }
              },
              "enabled": true,
              "ext": {
                "TemplateIDs": [
                  "58c2f62c34f5e387180003fa",
                  "57eea7983c5937912400002c",
                  "5ea53bae55ac4bba122eb2fd"
                ]
              },
              "buckets": [
                {
                  "_id": {
                    "$oid": "62de2e5498b0d630b11f8aee"
                  },
                  "name": "duration_0",
                  "weight": 0,
                  "ext": {
                    "duration": 0
                  }
                },
                {
                  "_id": {
                    "$oid": "62de32baed9740d20718748e"
                  },
                  "name": "duration_500",
                  "weight": 100,
                  "ext": {
                    "duration": 500
                  }
                }
              ],
              "app_whitelist": [
                "59786bc2a43b3a08620026b1",
                "59e781de7fff7cb02500ca0e"
              ],
              "placement_whitelist": []
            }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_that(normal_replacements['VIDEO_DELAY_DURATION'], equal_to('500'))

    @allure.feature('max latency experiment')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4458 AB testing to identify the Maximum Acceptable Latency between PlayAd and impression')
    @allure.description('Verify that Android pub app enter the experiment with duration token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_max_latency_exp_2(self, pub_app_id, placement):
        '''
            "templateId": "57eea7983c5937912400002c" from the mocked ad

            {
              "_id": {
                "$oid": "62de2db8bf51a2a06de84975"
              },
              "name": "Max_Latency_Experiment_phase1",
              "mutual_id": "62d4f4ef3571cd891d472cce",
              "allocate_strategy": "math_random",
              "salt": "62de2e2274b41f3c74958e5f",
              "countries": [],
              "is_all_countries": true,
              "is_all_applications": false,
              "traffic_percentage": 10000,
              "scope": "jaeger",
              "start_date": {
                "$date": {
                  "$numberLong": "1551398400000"
                }
              },
              "end_date": {
                "$date": {
                  "$numberLong": "4102444799999"
                }
              },
              "enabled": true,
              "ext": {
                "TemplateIDs": [
                  "58c2f62c34f5e387180003fa",
                  "57eea7983c5937912400002c",
                  "5ea53bae55ac4bba122eb2fd"
                ]
              },
              "buckets": [
                {
                  "_id": {
                    "$oid": "62de2e5498b0d630b11f8aee"
                  },
                  "name": "duration_0",
                  "weight": 0,
                  "ext": {
                    "duration": 0
                  }
                },
                {
                  "_id": {
                    "$oid": "62de32baed9740d20718748e"
                  },
                  "name": "duration_500",
                  "weight": 100,
                  "ext": {
                    "duration": 500
                  }
                }
              ],
              "app_whitelist": [
                "59786bc2a43b3a08620026b1",
                "59e781de7fff7cb02500ca0e"
              ],
              "placement_whitelist": []
            }
        '''
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_that(normal_replacements['VIDEO_DELAY_DURATION'], equal_to('500'))

    @allure.feature('max latency experiment')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4458 AB testing to identify the Maximum Acceptable Latency between PlayAd and impression')
    @allure.description('Verify that the pub app not on white list will not enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_max_latency_exp_3(self, pub_app_id, placement):
        '''
            {
              "_id": {
                "$oid": "62de2db8bf51a2a06de84975"
              },
              "name": "Max_Latency_Experiment_phase1",
              "mutual_id": "62d4f4ef3571cd891d472cce",
              "allocate_strategy": "math_random",
              "salt": "62de2e2274b41f3c74958e5f",
              "countries": [],
              "is_all_countries": true,
              "is_all_applications": false,
              "traffic_percentage": 10000,
              "scope": "jaeger",
              "start_date": {
                "$date": {
                  "$numberLong": "1551398400000"
                }
              },
              "end_date": {
                "$date": {
                  "$numberLong": "4102444799999"
                }
              },
              "enabled": true,
              "ext": {
                "TemplateIDs": [
                  "58c2f62c34f5e387180003fa",
                  "57eea7983c5937912400002c",
                  "5ea53bae55ac4bba122eb2fd"
                ]
              },
              "buckets": [
                {
                  "_id": {
                    "$oid": "62de2e5498b0d630b11f8aee"
                  },
                  "name": "duration_0",
                  "weight": 0,
                  "ext": {
                    "duration": 0
                  }
                },
                {
                  "_id": {
                    "$oid": "62de32baed9740d20718748e"
                  },
                  "name": "duration_500",
                  "weight": 100,
                  "ext": {
                    "duration": 500
                  }
                }
              ],
              "app_whitelist": [
                "59786bc2a43b3a08620026b1",
                "59e781de7fff7cb02500ca0e"
              ],
              "placement_whitelist": []
            }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_keys_not_exist(normal_replacements, 'VIDEO_DELAY_DURATION')

    @allure.feature('max latency experiment')
    @allure.tag('normal')
    @allure.story('PBJ-4458 AB testing to identify the Maximum Acceptable Latency between PlayAd and impression')
    @allure.description('Verify that the template id not on white list will not enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_max_latency_exp_4(self, pub_app_id, placement):
        '''
            {
              "_id": {
                "$oid": "62de2db8bf51a2a06de84975"
              },
              "name": "Max_Latency_Experiment_phase1",
              "mutual_id": "62d4f4ef3571cd891d472cce",
              "allocate_strategy": "math_random",
              "salt": "62de2e2274b41f3c74958e5f",
              "countries": [],
              "is_all_countries": true,
              "is_all_applications": false,
              "traffic_percentage": 10000,
              "scope": "jaeger",
              "start_date": {
                "$date": {
                  "$numberLong": "1551398400000"
                }
              },
              "end_date": {
                "$date": {
                  "$numberLong": "4102444799999"
                }
              },
              "enabled": true,
              "ext": {
                "TemplateIDs": [
                  "58c2f62c34f5e387180003fa",
                  "57eea7983c5937912400002c",
                  "5ea53bae55ac4bba122eb2fd"
                ]
              },
              "buckets": [
                {
                  "_id": {
                    "$oid": "62de2e5498b0d630b11f8aee"
                  },
                  "name": "duration_0",
                  "weight": 0,
                  "ext": {
                    "duration": 0
                  }
                },
                {
                  "_id": {
                    "$oid": "62de32baed9740d20718748e"
                  },
                  "name": "duration_500",
                  "weight": 100,
                  "ext": {
                    "duration": 500
                  }
                }
              ],
              "app_whitelist": [
                "59786bc2a43b3a08620026b1",
                "59e781de7fff7cb02500ca0e"
              ],
              "placement_whitelist": []
            }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_keys_not_exist(normal_replacements, 'VIDEO_DELAY_DURATION')

    @allure.feature('max latency experiment')
    @allure.tag('normal')
    @allure.story('PBJ-4458 AB testing to identify the Maximum Acceptable Latency between PlayAd and impression')
    @allure.description('Verify there is no limitation on eDSP when the app and template id are in white list')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_max_latency_exp_5(self, pub_app_id, placement):
        '''
            "templateId": "5ea53bae55ac4bba122eb2fd" from the mocked ad

            {
              "_id": {
                "$oid": "62de2db8bf51a2a06de84975"
              },
              "name": "Max_Latency_Experiment_phase1",
              "mutual_id": "62d4f4ef3571cd891d472cce",
              "allocate_strategy": "math_random",
              "salt": "62de2e2274b41f3c74958e5f",
              "countries": [],
              "is_all_countries": true,
              "is_all_applications": false,
              "traffic_percentage": 10000,
              "scope": "jaeger",
              "start_date": {
                "$date": {
                  "$numberLong": "1551398400000"
                }
              },
              "end_date": {
                "$date": {
                  "$numberLong": "4102444799999"
                }
              },
              "enabled": true,
              "ext": {
                "TemplateIDs": [
                  "58c2f62c34f5e387180003fa",
                  "57eea7983c5937912400002c",
                  "5ea53bae55ac4bba122eb2fd"
                ]
              },
              "buckets": [
                {
                  "_id": {
                    "$oid": "62de2e5498b0d630b11f8aee"
                  },
                  "name": "duration_0",
                  "weight": 0,
                  "ext": {
                    "duration": 0
                  }
                },
                {
                  "_id": {
                    "$oid": "62de32baed9740d20718748e"
                  },
                  "name": "duration_500",
                  "weight": 100,
                  "ext": {
                    "duration": 500
                  }
                }
              ],
              "app_whitelist": [
                "59786bc2a43b3a08620026b1",
                "59e781de7fff7cb02500ca0e"
              ],
              "placement_whitelist": []
            }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_that(normal_replacements['VIDEO_DELAY_DURATION'], equal_to('500'))

    @allure.feature('tpat clickUrl')
    @allure.tag('basic')
    @allure.story('PBJ-4333 Programmatic video - Add CTA_BUTTON_URL to tpat->clickUrl for EDSP ads.')
    @allure.description('Verify tapt clickUrl contains CTA_BUTTON_URL for sdk_version>=6.11.0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_tapt_clickUrl_contains_catButtonURl_01(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        cat_button_url = normal_replacements['CTA_BUTTON_URL']
        tpat_click_url = ad_markup['tpat']['clickUrl']
        assert_that(cat_button_url in tpat_click_url)

    @allure.feature('tpat clickUrl')
    @allure.tag('basic')
    @allure.story('PBJ-4333 Programmatic video - Add CTA_BUTTON_URL to tpat->clickUrl for EDSP ads.')
    @allure.description('Verify tapt clickUrl does not contain CTA_BUTTON_URL(apps.apple.com'
                        ') for sdk_version>=6.11.0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_tapt_clickUrl_contains_catButtonURl_02(self, pub_app_id, placement, sdk_v):
        override_adm = 'seatbid.0.bid.0.adm@"<VAST version=\\"2.0\\"><Ad><InLine><AdSystem><![CDATA[Bytedance]]><\\/AdSystem><AdTitle><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\/AdTitle><Impression><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/show_event\\/?req_id=5ec796d603e1e7c01267c88fu8791&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&source_type=1&pack_time=1590630440.65&pc=OMkaunPpDyKzZarhJKk3BmafV%2FjcG%2FID2AgSFwMkc6M%3D&ttdsp_price=${AUCTION_PRICE}]]><\\/Impression><Creatives><Creative id=\\"1665015151804428\\"><Linear><Duration>00:00:46<\\/Duration><TrackingEvents><Tracking event=\\"start\\"><![CDATA[https:\\/\\/is.snssdk.com\\/api\\/ad\\/union\\/event_report\\/?event_type=4&user_timezone={timezone}&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=0]]><\\/Tracking><Tracking event=\\"complete\\"><![CDATA[https:\\/\\/is.snssdk.com\\/api\\/ad\\/union\\/event_report\\/?event_type=6&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=27]]><\\/Tracking><Tracking event=\\"creativeView\\"><![CDATA[http:\\/\\/app05.adfalcon.com\\/E\\/78c1743833b34d43991083f92bd5b392_0_b338d452-96f4-4d37-b6e1-d10de8271ff4?ev=creativeview]]><\\/Tracking><\\/TrackingEvents><VideoClicks><ClickThrough><![CDATA[https:\\/\\/apps.apple.com\\/app\\/id]]><\\/ClickThrough><ClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=1&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/ClickTracking><CustomClick id=\\"ClickCoordinates-1\\"><![CDATA[https:\\/\\/c2.gdt.qq.com\\/gdt_mclick.fcg?viewid=!s6A4zH!POBbWj7ZQJudpxTBaTzOitZ8Zrj2cUWt!HRqifXlxVXVFYsSbE41QXp8NkVBskWi5Xu3It3wZDq05WhMsgfMLVxU41AQqVoe3wHYs6zZtEO_OtSDOHBiIm_Jn3xRWbR93zoDNI2kpylT7ltMreMCvonlVZ2Br0DCTf8SQOYklg8NNwTiMJCaTcC4xb7pIVEr5A5nkmccS3H9UpiMiJTk3eT_Yn57f4UxnMy9cxrAgVDosJFLJ6rXP6tZHCWVS3kSr0l5iRK1V956hwoVlIAVZCLcI!!qfcKzeS548ctKsM2Ps6ip5M9Cpx60&jtype=0&i=1&os=2&acttype=1&s={\\"req_width\\":\\"__REQ_WIDTH__\\",\\"req_height\\":\\"__REQ_HEIGHT__\\",\\"width\\":\\"__WIDTH__\\",\\"height\\":\\"__HEIGHT__\\",\\"down_x\\":\\"__DOWN_X__\\",\\"down_y\\":\\"__DOWN_Y__\\",\\"up_x\\":\\"__UP_X__\\",\\"up_y\\":\\"__UP_Y__\\"}&lpp=click_ext=eyJleHBfcGFyYW0iOiJjYXJyaWVyX2VuYWJsZToyIn0=&clklpp=__CLICK_LPP__&nxjp=1&cdnxj=1&xp=1&tl=1]]><\\/CustomClick><CustomClick id=\\"ClickCoordinates-2\\"><![CDATA[http:\\/\\/link\\/to\\/customclick\\/2]]><\\/CustomClick><CustomClick id=\\"customclick-3\\"><![CDATA[http:\\/\\/link\\/to\\/customclick\\/3]]><\\/CustomClick><\\/VideoClicks><MediaFiles><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[ asdjfklajsd;fkja;sdlkfjklasdjfklasdjfkl.mp4 ]]><\\/MediaFile><MediaFile bitrate=\\"206\\" delivery=\\"progressive\\" height=\\"180\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"320\\"><![CDATA[ test\\/jsldfjlksdfjk.mp4 ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[ v3-ad.ixigua.com\\/kghkhk\\/toutiao123werwerew.abc ]]><\\/MediaFile><MediaFile bitrate=\\"56\\" delivery=\\"progressive\\" height=\\"144\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"176\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/17\\/source\\/doubleclick_dmm\\/ctier\\/L\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748511\\/sparams\\/id,itag,source,ctier,ip,ipbits,expire\\/signature\\/8044BE9E3E1793FF36C03998BA13848E7C845ABE.75B6CAFBF57F6F96C78BDFCEB9653E601FD7E8D8\\/key\\/ck2\\/file\\/file.3gpp ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[https:\\/\\/v3-ad.ixigua.com\\/kghkhk\\/toutiao123]]><\\/MediaFile><MediaFile bitrate=\\"206\\" delivery=\\"progressive\\" height=\\"180\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"320\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/36\\/source\\/doubleclick_dmm\\/ctier\\/L\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748512\\/sparams\\/id,itag,source,ctier,ip,ipbits,expire\\/signature\\/29EC5A3574F0873D71FF75DEA54B89FD30A0D0B1.82B0C3EBBBAF7046A8DFBF3D94AAD9FC69C5C9A4\\/key\\/ck2\\/file\\/file.3gpp ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[https:\\/\\/cdn-cn.vungle.cn\\/zen\\/497a5dead8498d62d7c65967729639f7-1280x720-Q2.mp4]]><\\/MediaFile><MediaFile bitrate=\\"372\\" delivery=\\"progressive\\" height=\\"360\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/mp4\\" width=\\"640\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/18\\/source\\/doubleclick_dmm\\/ctier\\/L\\/acao\\/yes\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748513\\/sparams\\/id,itag,source,ctier,acao,ip,ipbits,expire\\/signature\\/484784AD6E9C1516EC07970AB978D11555654A9A.57EFB4F5F3CCE7F30CFBA1951E6434319300BE12\\/key\\/ck2\\/file\\/file.mp4 ]]><\\/MediaFile><MediaFile bitrate=\\"1879\\" delivery=\\"progressive\\" height=\\"720\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/mp4\\" width=\\"1280\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/22\\/source\\/doubleclick_dmm\\/ctier\\/L\\/acao\\/yes\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748528\\/sparams\\/id,itag,source,ctier,acao,ip,ipbits,expire\\/signature\\/7136B1FF2CD283E5A90276E455C5F970B91A35FF.8E6707BA3249059D7BA09F6E3D59FF6BA1D78FE0\\/key\\/ck2\\/file\\/file.mp4 ]]><\\/MediaFile><\\/MediaFiles><\\/Linear><\\/Creative><Creative><CompanionAds><Companion id=\\"post-roll\\" width=\\"1280\\" height=\\"720\\"><CompanionClickThrough><![CDATA[]]><\\/CompanionClickThrough><CompanionClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=2&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/CompanionClickTracking><TrackingEvents><Tracking event=\\"creativeView\\"><\\/Tracking><\\/TrackingEvents><StaticResource creativeType=\\"image\\/jpeg\\"><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/obj\\/mosaic-legacy\\/2ff3f000e60c223e67984]]><\\/StaticResource><\\/Companion><\\/CompanionAds><\\/Creative><\\/Creatives><Description><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\/Description><Survey><\\/Survey><Extensions><Extension type=\\"AdVerifications\\"><AdVerifications><Verification vendor=\\"moat.com-omsdkvungleinappvideo781943494431\\"><JavaScriptResource apiFramework=\\"omid\\" browserOptional=\\"true\\"><![CDATA[https:\\/\\/z.moatads.com\\/omsdkvungleinappvideo781943494431\\/moatvideo.js]]><\\/JavaScriptResource><VerificationParameters><![CDATA[{\\"moatClientLevel1\\":\\"{{{app_id}}}\\",\\"moatClientLevel2\\":\\"{{{campaign_id}}}\\",\\"moatClientLevel3\\":\\"{{{creative_id}}}\\",\\"moatClientLevel4\\":\\"{{{placement_id}}}\\",\\"moatClientSlicer1\\":\\"{{{pub_app_id}}}\\",\\"moatClientLevel5\\":\\"{{{rtb_deal_id}}}\\",\\"moatClientLevel6\\":\\"{{{rtb_connection_id}}}\\"}]]><\\/VerificationParameters><\\/Verification><\\/AdVerifications><\\/Extension><Extension type=\\"Extra\\"><CTA><![CDATA[\\u70B9\\u51FB\\u4E0B\\u8F7D]]><\\/CTA><SystemIcon><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/07c04164de3140d2cfe4bdd9812aef22~c1_0x0_q100.png]]><\\/SystemIcon><FullStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/48c275deda9f2daa92acccf8218fc59f~c1_0x0_q100.jpeg]]><\\/FullStar><HalfStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/b273598ab25fec09a467d2b895e3c53e~c1_0x0_q100.jpeg]]><\\/HalfStar><EmptyStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/fedbae142b79804e383eed3f4d06e9d5~c1_0x0_q100.jpeg]]><\\/EmptyStar><Review><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/297845a2690ec96bd1290a0a289ab373~c1_0x0_q100.jpeg]]><\\/Review><MoPubCtaText><\\/MoPubCtaText><\\/Extension><\\/Extensions><\\/InLine><\\/Ad><\\/VAST>"'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger', override_bid_response_any=override_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        cat_button_url = normal_replacements['CTA_BUTTON_URL']
        tpat_click_url = ad_markup['tpat']['clickUrl']
        assert_that(cat_button_url not in tpat_click_url)

    @allure.feature('tpat clickUrl')
    @allure.tag('basic')
    @allure.story('PBJ-4333 Programmatic video - Add CTA_BUTTON_URL to tpat->clickUrl for EDSP ads.')
    @allure.description('Verify tapt clickUrl does not contain CTA_BUTTON_URL(itunes.apple.com'
                        ') for sdk_version>=6.11.0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_tapt_clickUrl_contains_catButtonURl_03(self, pub_app_id, placement, sdk_v):
        override_adm = 'seatbid.0.bid.0.adm@"<VAST version=\\"2.0\\"><Ad><InLine><AdSystem><![CDATA[Bytedance]]><\\/AdSystem><AdTitle><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\/AdTitle><Impression><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/show_event\\/?req_id=5ec796d603e1e7c01267c88fu8791&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&source_type=1&pack_time=1590630440.65&pc=OMkaunPpDyKzZarhJKk3BmafV%2FjcG%2FID2AgSFwMkc6M%3D&ttdsp_price=${AUCTION_PRICE}]]><\\/Impression><Creatives><Creative id=\\"1665015151804428\\"><Linear><Duration>00:00:46<\\/Duration><TrackingEvents><Tracking event=\\"start\\"><![CDATA[https:\\/\\/is.snssdk.com\\/api\\/ad\\/union\\/event_report\\/?event_type=4&user_timezone={timezone}&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=0]]><\\/Tracking><Tracking event=\\"complete\\"><![CDATA[https:\\/\\/is.snssdk.com\\/api\\/ad\\/union\\/event_report\\/?event_type=6&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=27]]><\\/Tracking><Tracking event=\\"creativeView\\"><![CDATA[http:\\/\\/app05.adfalcon.com\\/E\\/78c1743833b34d43991083f92bd5b392_0_b338d452-96f4-4d37-b6e1-d10de8271ff4?ev=creativeview]]><\\/Tracking><\\/TrackingEvents><VideoClicks><ClickThrough><![CDATA[https:\\/\\/itunes.apple.com\\/app\\/id]]><\\/ClickThrough><ClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=1&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/ClickTracking><CustomClick id=\\"ClickCoordinates-1\\"><![CDATA[https:\\/\\/c2.gdt.qq.com\\/gdt_mclick.fcg?viewid=!s6A4zH!POBbWj7ZQJudpxTBaTzOitZ8Zrj2cUWt!HRqifXlxVXVFYsSbE41QXp8NkVBskWi5Xu3It3wZDq05WhMsgfMLVxU41AQqVoe3wHYs6zZtEO_OtSDOHBiIm_Jn3xRWbR93zoDNI2kpylT7ltMreMCvonlVZ2Br0DCTf8SQOYklg8NNwTiMJCaTcC4xb7pIVEr5A5nkmccS3H9UpiMiJTk3eT_Yn57f4UxnMy9cxrAgVDosJFLJ6rXP6tZHCWVS3kSr0l5iRK1V956hwoVlIAVZCLcI!!qfcKzeS548ctKsM2Ps6ip5M9Cpx60&jtype=0&i=1&os=2&acttype=1&s={\\"req_width\\":\\"__REQ_WIDTH__\\",\\"req_height\\":\\"__REQ_HEIGHT__\\",\\"width\\":\\"__WIDTH__\\",\\"height\\":\\"__HEIGHT__\\",\\"down_x\\":\\"__DOWN_X__\\",\\"down_y\\":\\"__DOWN_Y__\\",\\"up_x\\":\\"__UP_X__\\",\\"up_y\\":\\"__UP_Y__\\"}&lpp=click_ext=eyJleHBfcGFyYW0iOiJjYXJyaWVyX2VuYWJsZToyIn0=&clklpp=__CLICK_LPP__&nxjp=1&cdnxj=1&xp=1&tl=1]]><\\/CustomClick><CustomClick id=\\"ClickCoordinates-2\\"><![CDATA[http:\\/\\/link\\/to\\/customclick\\/2]]><\\/CustomClick><CustomClick id=\\"customclick-3\\"><![CDATA[http:\\/\\/link\\/to\\/customclick\\/3]]><\\/CustomClick><\\/VideoClicks><MediaFiles><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[ asdjfklajsd;fkja;sdlkfjklasdjfklasdjfkl.mp4 ]]><\\/MediaFile><MediaFile bitrate=\\"206\\" delivery=\\"progressive\\" height=\\"180\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"320\\"><![CDATA[ test\\/jsldfjlksdfjk.mp4 ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[ v3-ad.ixigua.com\\/kghkhk\\/toutiao123werwerew.abc ]]><\\/MediaFile><MediaFile bitrate=\\"56\\" delivery=\\"progressive\\" height=\\"144\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"176\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/17\\/source\\/doubleclick_dmm\\/ctier\\/L\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748511\\/sparams\\/id,itag,source,ctier,ip,ipbits,expire\\/signature\\/8044BE9E3E1793FF36C03998BA13848E7C845ABE.75B6CAFBF57F6F96C78BDFCEB9653E601FD7E8D8\\/key\\/ck2\\/file\\/file.3gpp ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[https:\\/\\/v3-ad.ixigua.com\\/kghkhk\\/toutiao123]]><\\/MediaFile><MediaFile bitrate=\\"206\\" delivery=\\"progressive\\" height=\\"180\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"320\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/36\\/source\\/doubleclick_dmm\\/ctier\\/L\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748512\\/sparams\\/id,itag,source,ctier,ip,ipbits,expire\\/signature\\/29EC5A3574F0873D71FF75DEA54B89FD30A0D0B1.82B0C3EBBBAF7046A8DFBF3D94AAD9FC69C5C9A4\\/key\\/ck2\\/file\\/file.3gpp ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[https:\\/\\/cdn-cn.vungle.cn\\/zen\\/497a5dead8498d62d7c65967729639f7-1280x720-Q2.mp4]]><\\/MediaFile><MediaFile bitrate=\\"372\\" delivery=\\"progressive\\" height=\\"360\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/mp4\\" width=\\"640\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/18\\/source\\/doubleclick_dmm\\/ctier\\/L\\/acao\\/yes\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748513\\/sparams\\/id,itag,source,ctier,acao,ip,ipbits,expire\\/signature\\/484784AD6E9C1516EC07970AB978D11555654A9A.57EFB4F5F3CCE7F30CFBA1951E6434319300BE12\\/key\\/ck2\\/file\\/file.mp4 ]]><\\/MediaFile><MediaFile bitrate=\\"1879\\" delivery=\\"progressive\\" height=\\"720\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/mp4\\" width=\\"1280\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/22\\/source\\/doubleclick_dmm\\/ctier\\/L\\/acao\\/yes\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748528\\/sparams\\/id,itag,source,ctier,acao,ip,ipbits,expire\\/signature\\/7136B1FF2CD283E5A90276E455C5F970B91A35FF.8E6707BA3249059D7BA09F6E3D59FF6BA1D78FE0\\/key\\/ck2\\/file\\/file.mp4 ]]><\\/MediaFile><\\/MediaFiles><\\/Linear><\\/Creative><Creative><CompanionAds><Companion id=\\"post-roll\\" width=\\"1280\\" height=\\"720\\"><CompanionClickThrough><![CDATA[]]><\\/CompanionClickThrough><CompanionClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=2&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/CompanionClickTracking><TrackingEvents><Tracking event=\\"creativeView\\"><\\/Tracking><\\/TrackingEvents><StaticResource creativeType=\\"image\\/jpeg\\"><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/obj\\/mosaic-legacy\\/2ff3f000e60c223e67984]]><\\/StaticResource><\\/Companion><\\/CompanionAds><\\/Creative><\\/Creatives><Description><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\/Description><Survey><\\/Survey><Extensions><Extension type=\\"AdVerifications\\"><AdVerifications><Verification vendor=\\"moat.com-omsdkvungleinappvideo781943494431\\"><JavaScriptResource apiFramework=\\"omid\\" browserOptional=\\"true\\"><![CDATA[https:\\/\\/z.moatads.com\\/omsdkvungleinappvideo781943494431\\/moatvideo.js]]><\\/JavaScriptResource><VerificationParameters><![CDATA[{\\"moatClientLevel1\\":\\"{{{app_id}}}\\",\\"moatClientLevel2\\":\\"{{{campaign_id}}}\\",\\"moatClientLevel3\\":\\"{{{creative_id}}}\\",\\"moatClientLevel4\\":\\"{{{placement_id}}}\\",\\"moatClientSlicer1\\":\\"{{{pub_app_id}}}\\",\\"moatClientLevel5\\":\\"{{{rtb_deal_id}}}\\",\\"moatClientLevel6\\":\\"{{{rtb_connection_id}}}\\"}]]><\\/VerificationParameters><\\/Verification><\\/AdVerifications><\\/Extension><Extension type=\\"Extra\\"><CTA><![CDATA[\\u70B9\\u51FB\\u4E0B\\u8F7D]]><\\/CTA><SystemIcon><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/07c04164de3140d2cfe4bdd9812aef22~c1_0x0_q100.png]]><\\/SystemIcon><FullStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/48c275deda9f2daa92acccf8218fc59f~c1_0x0_q100.jpeg]]><\\/FullStar><HalfStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/b273598ab25fec09a467d2b895e3c53e~c1_0x0_q100.jpeg]]><\\/HalfStar><EmptyStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/fedbae142b79804e383eed3f4d06e9d5~c1_0x0_q100.jpeg]]><\\/EmptyStar><Review><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/297845a2690ec96bd1290a0a289ab373~c1_0x0_q100.jpeg]]><\\/Review><MoPubCtaText><\\/MoPubCtaText><\\/Extension><\\/Extensions><\\/InLine><\\/Ad><\\/VAST>"'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger', override_bid_response_any=override_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        cat_button_url = normal_replacements['CTA_BUTTON_URL']
        tpat_click_url = ad_markup['tpat']['clickUrl']
        assert_that(cat_button_url not in tpat_click_url)

    @allure.feature('tpat clickUrl')
    @allure.tag('basic')
    @allure.story('PBJ-4622 allow DSP to pass clickURL in the bid response ext field to support banner/MREC storeKit '
                  'and endcard click_on_view')
    @allure.description('Verify eDSP pass clickUrl in the bid response: clicktrackers is not null')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_pass_clickUrl_from_bid_response_ext_01(self, pub_app_id, placement, sdk_v):
        clicktrackers = "https://emilytest.com"
        override_bid_response_any = 'seatbid.0.bid.0.ext.clicktrackers.0@"%s"' % clicktrackers
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=override_bid_response_any))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat_click_url = ad_markup['tpat']['clickUrl']
        assert_that(clicktrackers in tpat_click_url)

    @allure.feature('tpat clickUrl')
    @allure.tag('basic')
    @allure.story('PBJ-4622 allow DSP to pass clickURL in the bid response ext field to support banner/MREC storeKit '
                  'and endcard click_on_view')
    @allure.description('Verify eDSP pass clickUrl in the bid response: clicktrackers is []')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_pass_clickUrl_from_bid_response_ext_02(self, pub_app_id, placement, sdk_v):
        override_bid_response_any = 'seatbid.0.bid.0.ext.clicktrackers.0@'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=override_bid_response_any))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat_click_url = ad_markup['tpat']['clickUrl']
        assert_that("https://events.ads.vungle.com" in tpat_click_url[0])

    @allure.feature('tpat clickUrl')
    @allure.tag('basic')
    @allure.story('PBJ-4622 allow DSP to pass clickURL in the bid response ext field to support banner/MREC storeKit '
                  'and endcard click_on_view')
    @allure.description('Verify eDSP pass clickUrl in the bid response: clicktrackers is null')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_pass_clickUrl_from_bid_response_ext_03(self, pub_app_id, placement, sdk_v):
        override_bid_response_any = 'seatbid.0.bid.0.ext.clicktrackers@null'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=override_bid_response_any))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat_click_url = ad_markup['tpat']['clickUrl']
        assert_that("https://events.ads.vungle.com" in tpat_click_url[0])

    @allure.feature('tpat clickUrl')
    @allure.tag('basic')
    @allure.story(
        'PBJ-4622 allow DSP to pass clickURL in the bid response ext field to support banner/MREC storeKit and '
        'endcard click_on_view')
    @allure.description('Verify eDSP pass clickUrl in the bid response: clicktrackers.0 is not null')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_pass_clickUrl_from_bid_response_ext_05(self, pub_app_id, placement, sdk_v):
        clicktrackers = "https://emilytest.com"
        override_bid_response_any = 'seatbid.0.bid.0.ext.clicktrackers.0@"%s"' % clicktrackers
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=override_bid_response_any))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat_click_url = ad_markup['tpat']['clickUrl']
        assert_that(clicktrackers in tpat_click_url)

    @allure.feature('tpat clickUrl')
    @allure.tag('basic')
    @allure.story(
        'PBJ-4622 allow DSP to pass clickURL in the bid response ext field to support banner/MREC storeKit and '
        'endcard click_on_view')
    @allure.description('Verify eDSP pass clickUrl in the bid response: clicktrackers []')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_pass_clickUrl_from_bid_response_ext_06(self, pub_app_id, placement, sdk_v):
        override_bid_response_any = 'seatbid.0.bid.0.ext.clicktrackers.0@'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=override_bid_response_any))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat_click_url = ad_markup['tpat']['clickUrl']
        assert_that("https://lf.snssdk.com" in tpat_click_url[0])


    @allure.feature('MMP')
    @allure.tag('basic', 'v1.236.0')
    @allure.story(
        'PBJ-4621 [Programmatic] Firing click_on_view for the endcard of programmatic fullscreen template'
        'PBJ-4837 Allow DSP partners to opt-in / opt-out "Firing click_on_view for the endcard"'
    )
    @allure.description('Verify token \'EC_SKOVERLAY_DISABLE_AUTO_MMP\'="true" '
                        'for liftoff pass endcard.click_on_view=0 in bid response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_pass_click_on_view_02(self, pub_app_id, placement, sdk_v):
        '''

               :rtb setting:
               :allow_sko_autoclick_override_ec: true
               '''
        override_bid_response_any = 'seatbid.0.bid.0.ext.skadn.ext.skoverlay.show@1|||seatbid.0.bid.0.ext.skadn.ext.skoverlay.click_on_view@1|||seatbid.0.bid.0.ext.endcard.click_on_view@0'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=override_bid_response_any))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'EC_SKOVERLAY_DISABLE_AUTO_MMP')
        assert_that(normal_replacements['EC_SKOVERLAY_DISABLE_AUTO_MMP'], equal_to('true'))

    @allure.feature('MMP')
    @allure.tag('basic', 'v1.236.0')
    @allure.story(
        'PBJ-4621 [Programmatic] Firing click_on_view for the endcard of programmatic fullscreen template'
        'PBJ-4837 Allow DSP partners to opt-in / opt-out "Firing click_on_view for the endcard"')
    @allure.description('Verify token default value \'EC_SKOVERLAY_DISABLE_AUTO_MMP\'="true" '
                        'for liftoff pass endcard={} in bid response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_pass_click_on_view_endcard_03(self, pub_app_id, placement, sdk_v):
        #:allow_sko_autoclick_override_ec: true
        override_bid_response_any = 'seatbid.0.bid.0.ext.skadn.ext.skoverlay.show@1|||seatbid.0.bid.0.ext.skadn.ext.skoverlay.click_on_view@1|||seatbid.0.bid.0.ext.endcard.click_on_view@null'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=override_bid_response_any))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'EC_SKOVERLAY_DISABLE_AUTO_MMP')
        assert_that(normal_replacements['EC_SKOVERLAY_DISABLE_AUTO_MMP'], equal_to('true'))

    @allure.feature('MMP')
    @allure.tag('basic', 'v1.236.0')
    @allure.story(
        'PBJ-4621 [Programmatic] Firing click_on_view for the endcard of programmatic fullscreen template'
        'PBJ-4837 Allow DSP partners to opt-in / opt-out "Firing click_on_view for the endcard"')
    @allure.description('Verify token EC_SKOVERLAY_DISABLE_AUTO_MMP="true" whatever the value of endcard.click_on_view'
                        'for other edsps')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('click_on_view', [0, 1])
    @pytest.mark.parametrize('rtb',
                             [ext_non_test_mode_kraken_rtb_ids_vast_moloco, ext_non_test_mode_kraken_rtb_ids_vast])
    def test_pass_click_on_view_endcard_other_e_01(self, pub_app_id, placement, sdk_v, click_on_view, rtb):
        #:allow_sko_autoclick_override_ec: false
        override_bid_response_any = 'seatbid.0.bid.0.ext.skadn.ext.skoverlay.show@1|||seatbid.0.bid.0.ext.skadn.ext.skoverlay.click_on_view@1|||seatbid.0.bid.0.ext.endcard.click_on_view@%s' % click_on_view
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=override_bid_response_any))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'EC_SKOVERLAY_DISABLE_AUTO_MMP')
        assert_that(normal_replacements['EC_SKOVERLAY_DISABLE_AUTO_MMP'], equal_to('true'))

    @allure.feature('SKO')
    @allure.tag('basic', 'v1.245.0')
    @allure.story(
        'PBJ-4855 [Programmatic] Support SKO Auto delay on endcard through bid response')
    @allure.description('Verify token EC_SKOVERLAY_DELAY_SECONDS will rely on the dsp pass signal "companion_delay"')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('companion_delay', [0, 1, 5, 'null'])
    def test_pass_sko_delay_seconds_01(self, pub_app_id, placement, sdk_v, companion_delay):
        'bidext.skan.ext.skoverlay'
        override_bid_response_any = "seatbid.0.bid.0.ext.skadn.ext.skoverlay.show@1|||seatbid.0.bid.0.ext.skadn.ext.skoverlay.companion_delay@%s" % companion_delay
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=override_bid_response_any))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'EC_SKOVERLAY_DELAY_SECONDS')
        if companion_delay == 'null':
            assert_that(normal_replacements['EC_SKOVERLAY_DELAY_SECONDS'], equal_to(str(-1)))
        else:
            assert_that(normal_replacements['EC_SKOVERLAY_DELAY_SECONDS'], equal_to(str(companion_delay)))

    @allure.feature('normal replacements')
    @allure.tag('basic')
    @allure.story('PBJ-4886 Respect Placement Level "Display End Card" Setting for eDSP Ads')
    @allure.description('Verify that ')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_single_page])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_respect_placement_setting(self, pub_app_id, placement, sdk_v):
        """

        db setting:
        placement level:
        supported_template_types: ["single_page_fullscreen"]

        """
        over_ride_adm = 'seatbid.0.bid.0.attr.0@13|||seatbid.0.bid.0.adm@"<VAST version=\\\"2.0\\\"><Ad><InLine><AdSystem><![CDATA[Bytedance]]><\\\/AdSystem><AdTitle><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\\/AdTitle><Impression><![CDATA[https:\\\/\\\/lf.snssdk.com\\\/api\\\/ad\\\/union\\\/show_event\\\/?req_id=5ec796d603e1e7c01267c88fu8791&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&source_type=1&pack_time=1590630440.65&pc=OMkaunPpDyKzZarhJKk3BmafV%2FjcG%2FID2AgSFwMkc6M%3D&ttdsp_price=${AUCTION_PRICE}]]><\\\/Impression><Creatives><Creative id=\\\"1665015151804428\\\"><Linear><Duration>00:00:46<\\\/Duration><TrackingEvents><Tracking event=\\\"start\\\"><![CDATA[https:\\\/\\\/is.snssdk.com\\\/api\\\/ad\\\/union\\\/event_report\\\/?event_type=4&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=0]]><\\\/Tracking><Tracking event=\\\"complete\\\"><![CDATA[https:\\\/\\\/is.snssdk.com\\\/api\\\/ad\\\/union\\\/event_report\\\/?event_type=6&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=27]]><\\\/Tracking><Tracking event=\\\"creativeView\\\"><![CDATA[http:\\\/\\\/app05.adfalcon.com\\\/E\\\/78c1743833b34d43991083f92bd5b392_0_b338d452-96f4-4d37-b6e1-d10de8271ff4?ev=creativeview]]><\\\/Tracking><\\\/TrackingEvents><VideoClicks><ClickThrough><![CDATA[https:\\\/\\\/events-dca.bidder.kayzen.io\\\/click?raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\\/ClickThrough><ClickTracking><![CDATA[https:\\\/\\\/lf.snssdk.com\\\/api\\\/ad\\\/union\\\/redirect\\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=1&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\\/ClickTracking><CustomClick id=\\\"ClickCoordinates-1\\\"><![CDATA[https:\\\/\\\/c2.gdt.qq.com\\\/gdt_mclick.fcg?viewid=!s6A4zH!POBbWj7ZQJudpxTBaTzOitZ8Zrj2cUWt!HRqifXlxVXVFYsSbE41QXp8NkVBskWi5Xu3It3wZDq05WhMsgfMLVxU41AQqVoe3wHYs6zZtEO_OtSDOHBiIm_Jn3xRWbR93zoDNI2kpylT7ltMreMCvonlVZ2Br0DCTf8SQOYklg8NNwTiMJCaTcC4xb7pIVEr5A5nkmccS3H9UpiMiJTk3eT_Yn57f4UxnMy9cxrAgVDosJFLJ6rXP6tZHCWVS3kSr0l5iRK1V956hwoVlIAVZCLcI!!qfcKzeS548ctKsM2Ps6ip5M9Cpx60&jtype=0&i=1&os=2&acttype=1&s={\\\"req_width\\\":\\\"__REQ_WIDTH__\\\",\\\"req_height\\\":\\\"__REQ_HEIGHT__\\\",\\\"width\\\":\\\"__WIDTH__\\\",\\\"height\\\":\\\"__HEIGHT__\\\",\\\"down_x\\\":\\\"__DOWN_X__\\\",\\\"down_y\\\":\\\"__DOWN_Y__\\\",\\\"up_x\\\":\\\"__UP_X__\\\",\\\"up_y\\\":\\\"__UP_Y__\\\"}&lpp=click_ext=eyJleHBfcGFyYW0iOiJjYXJyaWVyX2VuYWJsZToyIn0=&clklpp=__CLICK_LPP__&nxjp=1&cdnxj=1&xp=1&tl=1]]><\\\/CustomClick><CustomClick id=\\\"ClickCoordinates-2\\\"><![CDATA[http:\\\/\\\/link\\\/to\\\/customclick\\\/2]]><\\\/CustomClick><CustomClick id=\\\"customclick-3\\\"><![CDATA[http:\\\/\\\/link\\\/to\\\/customclick\\\/3]]><\\\/CustomClick><\\\/VideoClicks><MediaFiles><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[ asdjfklajsd;fkja;sdlkfjklasdjfklasdjfkl.mp4 ]]><\\\/MediaFile><MediaFile bitrate=\\\"206\\\" delivery=\\\"progressive\\\" height=\\\"180\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/3gpp\\\" width=\\\"320\\\"><![CDATA[ test\\\/jsldfjlksdfjk.mp4 ]]><\\\/MediaFile><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[ v3-ad.ixigua.com\\\/kghkhk\\\/toutiao123werwerew.abc ]]><\\\/MediaFile><MediaFile bitrate=\\\"56\\\" delivery=\\\"progressive\\\" height=\\\"144\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/3gpp\\\" width=\\\"176\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/17\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748511\\\/sparams\\\/id,itag,source,ctier,ip,ipbits,expire\\\/signature\\\/8044BE9E3E1793FF36C03998BA13848E7C845ABE.75B6CAFBF57F6F96C78BDFCEB9653E601FD7E8D8\\\/key\\\/ck2\\\/file\\\/file.3gpp ]]><\\\/MediaFile><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[https:\\\/\\\/v3-ad.ixigua.com\\\/kghkhk\\\/toutiao123]]><\\\/MediaFile><MediaFile bitrate=\\\"206\\\" delivery=\\\"progressive\\\" height=\\\"180\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/3gpp\\\" width=\\\"320\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/36\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748512\\\/sparams\\\/id,itag,source,ctier,ip,ipbits,expire\\\/signature\\\/29EC5A3574F0873D71FF75DEA54B89FD30A0D0B1.82B0C3EBBBAF7046A8DFBF3D94AAD9FC69C5C9A4\\\/key\\\/ck2\\\/file\\\/file.3gpp ]]><\\\/MediaFile><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[https:\\\/\\\/cdn-cn.vungle.cn\\\/zen\\\/497a5dead8498d62d7c65967729639f7-1280x720-Q2.mp4]]><\\\/MediaFile><MediaFile bitrate=\\\"372\\\" delivery=\\\"progressive\\\" height=\\\"360\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/mp4\\\" width=\\\"640\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/18\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/acao\\\/yes\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748513\\\/sparams\\\/id,itag,source,ctier,acao,ip,ipbits,expire\\\/signature\\\/484784AD6E9C1516EC07970AB978D11555654A9A.57EFB4F5F3CCE7F30CFBA1951E6434319300BE12\\\/key\\\/ck2\\\/file\\\/file.mp4 ]]><\\\/MediaFile><MediaFile bitrate=\\\"1879\\\" delivery=\\\"progressive\\\" height=\\\"720\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/22\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/acao\\\/yes\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748528\\\/sparams\\\/id,itag,source,ctier,acao,ip,ipbits,expire\\\/signature\\\/7136B1FF2CD283E5A90276E455C5F970B91A35FF.8E6707BA3249059D7BA09F6E3D59FF6BA1D78FE0\\\/key\\\/ck2\\\/file\\\/file.mp4 ]]><\\\/MediaFile><\\\/MediaFiles><\\\/Linear><\\\/Creative><Creative><CompanionAds><Companion width=\\\"480\\\" height=\\\"320\\\"><HTMLResource><![CDATA[<div style=\\\"position:absolute;top:0;bottom:0;left:0;right:0;\\\"><meta charset=\\\"utf-8\\\"\\\/><meta name=\\\"viewport\\\" content=\\\"width=device-width,initial-scale=1,user-scalable=no\\\"\\\/><a id=\\\"exchange-ping-url\\\" href=\\\"https:\\\/\\\/cdn.liftoff.io\\\/tracking_pixel.gif\\\" style=\\\"display:none\\\"><\\\/a><script>window.LIFTOFF_START_TS = Date.now()<\\\/script><script src=\\\"https:\\\/\\\/cdn.liftoff.io\\\/resources\\\/polyfills-33c384a010d661c2a64d.js\\\"><\\\/script><div id=\\\"tracking-tag-holder\\\" style=\\\"display:none\\\"><\\\/div><script src=\\\"https:\\\/\\\/cdn.liftoff.io\\\/resources\\\/outer_env-aae1d794a14769f5efcc.js\\\"><\\\/script><div id=\\\"liftoff-snippet\\\"><\\\/div><script>LiftoffOuterEnv.init({inProd: true,containerEl: document.getElementById(\\\"liftoff-snippet\\\"),envData: JSON.parse(decodeURIComponent(\'{\\\"clickURLs\\\":{\\\"clickthroughURL\\\":{\\\"url\\\":\\\"https:\\\/\\\/play.google.com\\\/store\\\/apps\\\/details%3Fid=com.playrix.township\\\",\\\"type\\\":2},\\\"clickTrackingURLs\\\":%5B{\\\"url\\\":\\\"https:\\\/\\\/click.liftoff.io\\\/v1\\\/campaign_click\\\/Mg7kXlNeI6IpbPMmKzZY_ztMYM6NO1OeUtL7NsADF-hcIl_fVATEOtZ5jelfNO7I3TKARpSfHHHxEXfDLJalv9ui50FzdKTT3J15quufe6oxCz-RHA4LAZH70RhIJ6E29NjJFl0lG_8JKgaH29DOceobtRV7Um0DSfKEnyyGHg_P87C3QOyQLZD4oIlLSpdfr0BBoUvH_3yIq9WNf6VG6eltwUSDd_ONKwaeEjbX0pCLDTr9R-HIfxpmb4LyTx0otoP6tRnS-QrE0tYnlFpMyjcHaArwt2f6_48fwWEdREjOVek8RDeptq7HNiOnRVLbbCdWXb9F1isw9jjphxlFEZZOhGU10iRpylSmKZw7WmPt2EVhcdsy_KWhe-KkNXWm-O8PUzqZNxKoM9-z5wgbZmJrOdgq0IHbbY-iQQVr640w3mPnnoGqGZBAj8PS2CLGNDCd8oCFe0PuQpsykAJ4ZeUwrq3S7TOvKqpd5_Bcpb1_pXitJ7UBh7l4yeb5gl9udGXyE02dysrtz2BICk4Rvopw2FwPPXWlEWsOF-lkx2QYQ9Pu2Y5MYa62ow0qqhcaogU6uj0ghqKqjG_mfw%3Fvast_el=3\\\",\\\"type\\\":1}%5D},\\\"costModel\\\":null,\\\"pinpointURL\\\":\\\"https:\\\/\\\/play.google.com\\\/store\\\/apps\\\/details%3Fid=com.playrix.township\\\",\\\"isReengagement\\\":false,\\\"impression\\\":{\\\"auctionID\\\":\\\"61516e15294ecded58f89c8e\\\",\\\"isRewarded\\\":true},\\\"loggingConfig\\\":{\\\"enableHTMLReturn\\\":false,\\\"eventTrackingParam\\\":\\\"c9dfb5CN3VBxIYNjE1MTZlMTUyOTRlY2RlZDU4Zjg5YzhlGIiE2LDCLyAYKPuCDTCbCzoiY29tLm9zLmZhbGNvbi5ib2IyLmFkdmVudHVyZS53b3JsZEIaY2xpY2std2F0ZXJmYWxsLXYyLWNvbnRyb2xCG3Zhc3QtaHRtbC1lbmRzY3JlZW4tY29udHJvbEIcaW9zLWh0bWwtbWV0YS1oZWFkZXItY29udHJvbEIbY3NwLXNyY2RvYy1wcmlvcml0eS1jb250cm9sQhdhcHAtc3RvcmUtbW9kYWwtY29udHJvbEoKNDFjMjE4YjEzNFADWgNJRE5gAmgEcg5hcC1ub3J0aGVhc3QtMYABGJIBAmlkmAECoQEzMzMzMzOzP6oBCDE2NDB4ODEwsgEJQWR2ZW50dXJlugEcQm9iJ3MgV29ybGQgMiAtIFJ1bm5pbmcgZ2FtZcIBGXZhc3QtY2RiNDU5ZDNjNjViMTdkODdlMGLKAQIBAtIBAA\\\",\\\"htmlReturnDelay\\\":\\\"5000\\\",\\\"enableLogging\\\":true,\\\"loggingEndpoint\\\":\\\"https:\\\/\\\/adexp.liftoff.io\\\"},\\\"clickConfig\\\":{\\\"clickthroughURL\\\":{\\\"url\\\":\\\"https:\\\/\\\/play.google.com\\\/store\\\/apps\\\/details%3Fid=com.playrix.township\\\",\\\"type\\\":2},\\\"clickTrackingURLs\\\":%5B{\\\"url\\\":\\\"https:\\\/\\\/click.liftoff.io\\\/v1\\\/campaign_click\\\/Mg7kXlNeI6IpbPMmKzZY_ztMYM6NO1OeUtL7NsADF-hcIl_fVATEOtZ5jelfNO7I3TKARpSfHHHxEXfDLJalv9ui50FzdKTT3J15quufe6oxCz-RHA4LAZH70RhIJ6E29NjJFl0lG_8JKgaH29DOceobtRV7Um0DSfKEnyyGHg_P87C3QOyQLZD4oIlLSpdfr0BBoUvH_3yIq9WNf6VG6eltwUSDd_ONKwaeEjbX0pCLDTr9R-HIfxpmb4LyTx0otoP6tRnS-QrE0tYnlFpMyjcHaArwt2f6_48fwWEdREjOVek8RDeptq7HNiOnRVLbbCdWXb9F1isw9jjphxlFEZZOhGU10iRpylSmKZw7WmPt2EVhcdsy_KWhe-KkNXWm-O8PUzqZNxKoM9-z5wgbZmJrOdgq0IHbbY-iQQVr640w3mPnnoGqGZBAj8PS2CLGNDCd8oCFe0PuQpsykAJ4ZeUwrq3S7TOvKqpd5_Bcpb1_pXitJ7UBh7l4yeb5gl9udGXyE02dysrtz2BICk4Rvopw2FwPPXWlEWsOF-lkx2QYQ9Pu2Y5MYa62ow0qqhcaogU6uj0ghqKqjG_mfw%3Fvast_el=3\\\",\\\"type\\\":1}%5D},\\\"cdnURL\\\":\\\"https:\\\/\\\/cdn.liftoff.io\\\",\\\"geo\\\":{\\\"latitude\\\":-7.2484,\\\"longitude\\\":112.7419},\\\"creative\\\":{\\\"id\\\":213371,\\\"width\\\":480,\\\"height\\\":320,\\\"name\\\":\\\"%28image211%29480x320_ts_video661v1_nst_en_30s_20mb_options_playable124\\\",\\\"params\\\":%5B%5D},\\\"abTests\\\":%5B\\\"click-waterfall-v2-control\\\",\\\"vast-html-endscreen-control\\\",\\\"ios-html-meta-header-control\\\",\\\"csp-srcdoc-priority-control\\\",\\\"app-store-modal-control\\\"%5D,\\\"app\\\":{\\\"id\\\":\\\"com.os.falcon.bob2.adventure.world\\\",\\\"name\\\":\\\"Bob%27s World 2 - Running game\\\"},\\\"campaign\\\":{\\\"id\\\":15373,\\\"name\\\":\\\"TS_GP_AP_Low\\\",\\\"params\\\":%5B%5D},\\\"creativePolicy\\\":{\\\"animationDurationLimit\\\":0,\\\"audioPolicy\\\":\\\"always-mute\\\",\\\"russianAgeRating\\\":null,\\\"removeAdWrapper\\\":false,\\\"showAdChoices\\\":false,\\\"addBorder\\\":false,\\\"useCustomClose\\\":false,\\\"closeDelay\\\":5,\\\"blockNotifications\\\":false,\\\"showChineseWatermark\\\":false,\\\"blockStrobing\\\":false},\\\"device\\\":{\\\"googleAID\\\":\\\"aa9f2aa4-845d-4bfe-bc6b-9150e1b1551d\\\",\\\"connectionType\\\":3,\\\"googleAIDSHA1\\\":\\\"b34af918dd77461b498a5af0e54d84895de14ed8\\\",\\\"ip\\\":\\\"112.215.237.195\\\",\\\"idfaSHA1\\\":null,\\\"androidIDMD5\\\":null,\\\"idfa\\\":null,\\\"normalizedLanguage\\\":\\\"id\\\",\\\"osVersion\\\":\\\"11\\\",\\\"idfaMD5\\\":null,\\\"androidIDSHA1\\\":null,\\\"androidID\\\":null,\\\"platform\\\":\\\"android\\\",\\\"model\\\":\\\"\\\"},\\\"trackingToken\\\":\\\"v.2_g.125661_a.61516e15294ecded58f89c8e_c.24_t.ua_u.b34af918dd77461b\\\",\\\"exchange\\\":\\\"vungle\\\",\\\"isStaffDevice\\\":false,\\\"platform\\\":\\\"android\\\"}\')),scriptSrcURLs: [\\\"https:\\\/\\\/cdn.liftoff.io\\\/resources\\\/polyfills-33c384a010d661c2a64d.js\\\",\\\"https:\\\/\\\/cdn.liftoff.io\\\/resources\\\/inner_env-bfa56fb84006156f82f7.js\\\"],rootURL: \\\"https:\\\/\\\/cdn.liftoff.io\\\/customers\\\/753\\\/creatives\\\/205394\\\/\\\",html: \'%3C%21DOCTYPE html%3E%3Chtml%3E%3Chead%3E%3Cmeta charset=\\\"utf-8\\\"%3E%3Ctitle%3EPlayable%3C\\\/title%3E%3Cmeta name=\\\"viewport\\\" content=\\\"width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover\\\"%3E%3C\\\/head%3E%3Cbody%3E%3Cscript type=\\\"text\\\/javascript\\\"%3Ewindow.apiName=\\\"liftoff\\\"%3Bwindow.playableEnv={\\\"lang\\\":\\\"en\\\",\\\"apiName\\\":\\\"liftoff\\\",\\\"nameGameAbbr\\\":\\\"ts\\\",\\\"params\\\":{\\\"showInstallButton\\\":true}}%3C\\\/script%3E%3Cdiv id=\\\"styles-container\\\"%3E%3C\\\/div%3E%3Cdiv id=\\\"scripts-container\\\"%3E%3C\\\/div%3E%3Cscript type=\\\"text\\\/javascript\\\"%3Ewindow.addEventListener%28\\\"load\\\",function%28%29{var is_ready_app,is_ready_timer,ROOT_URL=\\\"\\\"%3B\\\"undefined\\\"%21=typeof LIFTOFF_ROOT_URL%26%26%28ROOT_URL=LIFTOFF_ROOT_URL%29%3Bvar name,cb,style,counter=0%3Bfunction next%28%29{loader.create%28%29,setTimeout%28function%28%29{is_ready_timer=%210,init%28%29},1e3%29,js%28\\\"app.js\\\",function%28%29{is_ready_app=%210,init%28%29}%29}function init%28%29{is_ready_timer%26%26is_ready_app%26%26%28\\\"undefined\\\"%21=typeof superApp%3FsuperApp.init%28%29:initGame%28%29,\\\"undefined\\\"%21=typeof loader%26%26loader.clear%28%29%29}function js%28name,cb%29{var script=document.createElement%28\\\"script\\\"%29%3Bscript.src=ROOT_URL+name,document.getElementById%28\\\"scripts-container\\\"%29.appendChild%28script%29,script.onload=function%28%29{cb%26%26cb%28%29}}js%28\\\"loader.js\\\",function%28%29{2==++counter%26%26next%28%29}%29,name=\\\"styles.css\\\",cb=function%28%29{2==++counter%26%26next%28%29},%28style=document.createElement%28\\\"link\\\"%29%29.href=ROOT_URL+name,style.type=\\\"text\\\/css\\\",style.rel=\\\"stylesheet\\\",style.media=\\\"screen,print\\\",document.getElementById%28\\\"styles-container\\\"%29.appendChild%28style%29,style.onload=function%28%29{cb%26%26cb%28%29},window.clickInstall=function%28%29{window.open%28window._LIFTOFF_ENV.pinpointURL,\\\"_blank\\\"%29}}%29%3B%3C\\\/script%3E%3C\\\/body%3E%3C\\\/html%3E\',externalHtmlURL: null,});<\\\/script><\\\/div>]]><\\\/HTMLResource><TrackingEvents><Tracking event=\\\"creativeView\\\"><![CDATA[https:\\\/\\\/adexp.liftoff.io\\\/event\\\/vast\\\/htmlEndscreenView\\\/c9dfb5CN3VBxIYNjE1MTZlMTUyOTRlY2RlZDU4Zjg5YzhlGIiE2LDCLyAYKPuCDTCbCzoiY29tLm9zLmZhbGNvbi5ib2IyLmFkdmVudHVyZS53b3JsZEIaY2xpY2std2F0ZXJmYWxsLXYyLWNvbnRyb2xCG3Zhc3QtaHRtbC1lbmRzY3JlZW4tY29udHJvbEIcaW9zLWh0bWwtbWV0YS1oZWFkZXItY29udHJvbEIbY3NwLXNyY2RvYy1wcmlvcml0eS1jb250cm9sQhdhcHAtc3RvcmUtbW9kYWwtY29udHJvbEoKNDFjMjE4YjEzNFADWgNJRE5gAmgEcg5hcC1ub3J0aGVhc3QtMYABGJIBAmlkmAECoQEzMzMzMzOzP6oBCDE2NDB4ODEwsgEJQWR2ZW50dXJlugEcQm9iJ3MgV29ybGQgMiAtIFJ1bm5pbmcgZ2FtZcIBGXZhc3QtY2RiNDU5ZDNjNjViMTdkODdlMGLKAQIBAtIBAA?playhead=[CONTENTPLAYHEAD]&sr=1]]><\\\/Tracking><\\\/TrackingEvents><\\\/Companion><\\\/CompanionAds><\\\/Creative><\\\/Creatives><Description><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\\/Description><Survey><\\\/Survey><Extensions><Extension type=\\\"AdVerifications\\\"><AdVerifications><Verification vendor=\\\"moat.com-omsdkvungleinappvideo781943494431\\\"><JavaScriptResource apiFramework=\\\"omid\\\" browserOptional=\\\"true\\\"><![CDATA[https:\\\/\\\/z.moatads.com\\\/omsdkvungleinappvideo781943494431\\\/moatvideo.js]]><\\\/JavaScriptResource><VerificationParameters><![CDATA[{\\\"moatClientLevel1\\\":\\\"{{{app_id}}}\\\",\\\"moatClientLevel2\\\":\\\"{{{campaign_id}}}\\\",\\\"moatClientLevel3\\\":\\\"{{{creative_id}}}\\\",\\\"moatClientLevel4\\\":\\\"{{{placement_id}}}\\\",\\\"moatClientSlicer1\\\":\\\"{{{pub_app_id}}}\\\",\\\"moatClientLevel5\\\":\\\"{{{rtb_deal_id}}}\\\",\\\"moatClientLevel6\\\":\\\"{{{rtb_connection_id}}}\\\"}]]><\\\/VerificationParameters><\\\/Verification><\\\/AdVerifications><\\\/Extension><Extension type=\\\"Extra\\\"><CTA><![CDATA[\\u70B9\\u51FB\\u4E0B\\u8F7D]]><\\\/CTA><SystemIcon><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/07c04164de3140d2cfe4bdd9812aef22~c1_0x0_q100.png]]><\\\/SystemIcon><FullStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/48c275deda9f2daa92acccf8218fc59f~c1_0x0_q100.jpeg]]><\\\/FullStar><HalfStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/b273598ab25fec09a467d2b895e3c53e~c1_0x0_q100.jpeg]]><\\\/HalfStar><EmptyStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/fedbae142b79804e383eed3f4d06e9d5~c1_0x0_q100.jpeg]]><\\\/EmptyStar><Review><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/297845a2690ec96bd1290a0a289ab373~c1_0x0_q100.jpeg]]><\\\/Review><MoPubCtaText><\\\/MoPubCtaText><\\\/Extension><\\\/Extensions><\\\/InLine><\\\/Ad><\\\/VAST>"'
        over_ride_adm = over_ride_adm.replace("\\\\", "\\")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, "VX_ENDCARD")
        assert_keys_not_exist(normal_replacements, "EC_HTML")

    @allure.feature('normal replacements')
    @allure.tag('basic')
    @allure.story('PBJ-5074 Amend Privacy related information by SSP')
    @allure.description('Verify that privacy releated tokens has been removed')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_remove_privacy_tokens_01(self, pub_app_id, placement, sdk_v):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, 'PRIVACY_BODY_TEXT')
        assert_keys_not_exist(normal_replacements, 'PRIVACY_CLOSE_TEXT')
        assert_keys_not_exist(normal_replacements, 'PRIVACY_CONTINUE_TEXT')
        assert_keys_exist(normal_replacements, 'VUNGLE_PRIVACY_URL')
        assert_that(normal_replacements['VUNGLE_PRIVACY_URL'], equal_to('https://privacy.liftoff.io/'))

    @allure.feature('normal replacements')
    @allure.tag('basic', 'test mode')
    @allure.story('PBJ-5074 Amend Privacy related information by SSP')
    @allure.description('Verify that privacy releated tokens has been removed')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_remove_privacy_tokens_02(self, pub_app_id, placement, sdk_v):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, 'PRIVACY_BODY_TEXT')
        assert_keys_not_exist(normal_replacements, 'PRIVACY_CLOSE_TEXT')
        assert_keys_not_exist(normal_replacements, 'PRIVACY_CONTINUE_TEXT')
        assert_keys_exist(normal_replacements, 'VUNGLE_PRIVACY_URL')
        assert_that(normal_replacements['VUNGLE_PRIVACY_URL'], equal_to('https://privacy.liftoff.io/'))

    @allure.feature('normal replacements')
    @allure.tag('basic')
    @allure.story('PBJ-5074 Amend Privacy related information by SSP')
    @allure.description('Verify that privacy releated tokens has been removed')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_remove_privacy_tokens_01(self, pub_app_id, placement, sdk_v):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, 'PRIVACY_BODY_TEXT')
        assert_keys_not_exist(normal_replacements, 'PRIVACY_CLOSE_TEXT')
        assert_keys_not_exist(normal_replacements, 'PRIVACY_CONTINUE_TEXT')
        assert_keys_exist(normal_replacements, 'VUNGLE_PRIVACY_URL')
        assert_that(normal_replacements['VUNGLE_PRIVACY_URL'], equal_to('https://privacy.liftoff.io/'))

    @allure.feature('normal replacements')
    @allure.tag('basic', 'test mode')
    @allure.story('PBJ-5074 Amend Privacy related information by SSP')
    @allure.description('Verify that privacy releated tokens has been removed')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_remove_privacy_tokens_02(self, pub_app_id, placement, sdk_v):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, 'PRIVACY_BODY_TEXT')
        assert_keys_not_exist(normal_replacements, 'PRIVACY_CLOSE_TEXT')
        assert_keys_not_exist(normal_replacements, 'PRIVACY_CONTINUE_TEXT')
        assert_keys_exist(normal_replacements, 'VUNGLE_PRIVACY_URL')
        assert_that(normal_replacements['VUNGLE_PRIVACY_URL'], equal_to('https://privacy.liftoff.io/'))

    @allure.feature('programmatic Static Endcard')
    @allure.tag('basic')
    @allure.story('PBJ-5045 Add "close button delay control" for the last chance endcard (3rd page EC) for eDSP ads')
    @allure.description('Verify "EC_CLOSE_BUTTON_DELAY_SECONDS" in case of the vungle endcard as 2nd page endcard')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_vx_2nd_colse_button_delay_01(self, pub_app_id, placement, sdk_v, rtb_ids):
        """
        setting in dashboard:
        app level:
        allow_static_endcard: true
        adExperience.multi_ec_close_button_delay:11


        placement level:
        multi_ec_close_button_delay:16
        """
        over_ride_adm = 'seatbid.0.bid.0.adm@"<VAST version=\\\"2.0\\\"><Ad><InLine><AdSystem><![CDATA[Bytedance]]><\\\/AdSystem><AdTitle><![CDATA[Bytedance]]><\\\/AdTitle><Impression><![CDATA[https:\\\/\\\/lf.snssdk.com\\\/api\\\/ad\\\/union\\\/show_event\\\/?req_id=5ec796d603e1e7c01267c88fu8791&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&source_type=1&pack_time=1590630440.65&pc=OMkaunPpDyKzZarhJKk3BmafV%2FjcG%2FID2AgSFwMkc6M%3D&ttdsp_price=${AUCTION_PRICE}]]><\\\/Impression><Creatives><Creative id=\\\"1665015151804428\\\"><Linear><Duration>00:00:46<\\\/Duration><TrackingEvents><Tracking event=\\\"start\\\"><![CDATA[https:\\\/\\\/is.snssdk.com\\\/api\\\/ad\\\/union\\\/event_report\\\/?event_type=4&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=0]]><\\\/Tracking><Tracking event=\\\"complete\\\"><![CDATA[https:\\\/\\\/is.snssdk.com\\\/api\\\/ad\\\/union\\\/event_report\\\/?event_type=6&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=27]]><\\\/Tracking><Tracking event=\\\"creativeView\\\"><![CDATA[http:\\\/\\\/app05.adfalcon.com\\\/E\\\/78c1743833b34d43991083f92bd5b392_0_b338d452-96f4-4d37-b6e1-d10de8271ff4?ev=creativeview]]><\\\/Tracking><\\\/TrackingEvents><VideoClicks><ClickThrough><![CDATA[https:\\\/\\\/events-dca.bidder.kayzen.io\\\/click?raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\\/ClickThrough><ClickTracking><![CDATA[https:\\\/\\\/lf.snssdk.com\\\/api\\\/ad\\\/union\\\/redirect\\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=1&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\\/ClickTracking><CustomClick id=\\\"ClickCoordinates-1\\\"><![CDATA[https:\\\/\\\/c2.gdt.qq.com\\\/gdt_mclick.fcg?viewid=!s6A4zH!POBbWj7ZQJudpxTBaTzOitZ8Zrj2cUWt!HRqifXlxVXVFYsSbE41QXp8NkVBskWi5Xu3It3wZDq05WhMsgfMLVxU41AQqVoe3wHYs6zZtEO_OtSDOHBiIm_Jn3xRWbR93zoDNI2kpylT7ltMreMCvonlVZ2Br0DCTf8SQOYklg8NNwTiMJCaTcC4xb7pIVEr5A5nkmccS3H9UpiMiJTk3eT_Yn57f4UxnMy9cxrAgVDosJFLJ6rXP6tZHCWVS3kSr0l5iRK1V956hwoVlIAVZCLcI!!qfcKzeS548ctKsM2Ps6ip5M9Cpx60&jtype=0&i=1&os=2&acttype=1&s={\\\"req_width\\\":\\\"__REQ_WIDTH__\\\",\\\"req_height\\\":\\\"__REQ_HEIGHT__\\\",\\\"width\\\":\\\"__WIDTH__\\\",\\\"height\\\":\\\"__HEIGHT__\\\",\\\"down_x\\\":\\\"__DOWN_X__\\\",\\\"down_y\\\":\\\"__DOWN_Y__\\\",\\\"up_x\\\":\\\"__UP_X__\\\",\\\"up_y\\\":\\\"__UP_Y__\\\"}&lpp=click_ext=eyJleHBfcGFyYW0iOiJjYXJyaWVyX2VuYWJsZToyIn0=&clklpp=__CLICK_LPP__&nxjp=1&cdnxj=1&xp=1&tl=1]]><\\\/CustomClick><CustomClick id=\\\"ClickCoordinates-2\\\"><![CDATA[http:\\\/\\\/link\\\/to\\\/customclick\\\/2]]><\\\/CustomClick><CustomClick id=\\\"customclick-3\\\"><![CDATA[http:\\\/\\\/link\\\/to\\\/customclick\\\/3]]><\\\/CustomClick><\\\/VideoClicks><MediaFiles><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[https:\\\/\\\/cdn-cn.vungle.cn\\\/zen\\\/497a5dead8498d62d7c65967729639f7-1280x720-Q2.mp4]]><\\\/MediaFile><MediaFile bitrate=\\\"372\\\" delivery=\\\"progressive\\\" height=\\\"360\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/mp4\\\" width=\\\"640\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/18\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/acao\\\/yes\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748513\\\/sparams\\\/id,itag,source,ctier,acao,ip,ipbits,expire\\\/signature\\\/484784AD6E9C1516EC07970AB978D11555654A9A.57EFB4F5F3CCE7F30CFBA1951E6434319300BE12\\\/key\\\/ck2\\\/file\\\/file.mp4 ]]><\\\/MediaFile><MediaFile bitrate=\\\"1879\\\" delivery=\\\"progressive\\\" height=\\\"720\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/22\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/acao\\\/yes\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748528\\\/sparams\\\/id,itag,source,ctier,acao,ip,ipbits,expire\\\/signature\\\/7136B1FF2CD283E5A90276E455C5F970B91A35FF.8E6707BA3249059D7BA09F6E3D59FF6BA1D78FE0\\\/key\\\/ck2\\\/file\\\/file.mp4 ]]><\\\/MediaFile><\\\/MediaFiles><\\\/Linear><\\\/Creative><\\\/Creatives><Description><![CDATA[Bytedance]]><\\\/Description><Survey><\\\/Survey><Extensions><Extension type=\\\"AdVerifications\\\"><AdVerifications><Verification vendor=\\\"moat.com-omsdkvungleinappvideo781943494431\\\"><JavaScriptResource apiFramework=\\\"omid\\\" browserOptional=\\\"true\\\"><![CDATA[https:\\\/\\\/z.moatads.com\\\/omsdkvungleinappvideo781943494431\\\/moatvideo.js]]><\\\/JavaScriptResource><VerificationParameters><![CDATA[{\\\"moatClientLevel1\\\":\\\"{{{app_id}}}\\\",\\\"moatClientLevel2\\\":\\\"{{{campaign_id}}}\\\",\\\"moatClientLevel3\\\":\\\"{{{creative_id}}}\\\",\\\"moatClientLevel4\\\":\\\"{{{placement_id}}}\\\",\\\"moatClientSlicer1\\\":\\\"{{{pub_app_id}}}\\\",\\\"moatClientLevel5\\\":\\\"{{{rtb_deal_id}}}\\\",\\\"moatClientLevel6\\\":\\\"{{{rtb_connection_id}}}\\\"}]]><\\\/VerificationParameters><\\\/Verification><\\\/AdVerifications><\\\/Extension><Extension type=\\\"Extra\\\"><CTA><![CDATA[Bytedance]]><\\\/CTA><SystemIcon><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/07c04164de3140d2cfe4bdd9812aef22~c1_0x0_q100.png]]><\\\/SystemIcon><FullStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/48c275deda9f2daa92acccf8218fc59f~c1_0x0_q100.jpeg]]><\\\/FullStar><HalfStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/b273598ab25fec09a467d2b895e3c53e~c1_0x0_q100.jpeg]]><\\\/HalfStar><EmptyStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/fedbae142b79804e383eed3f4d06e9d5~c1_0x0_q100.jpeg]]><\\\/EmptyStar><Review><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/297845a2690ec96bd1290a0a289ab373~c1_0x0_q100.jpeg]]><\\\/Review><MoPubCtaText><\\\/MoPubCtaText><\\\/Extension><Extension type=\\\"Vungle\\\"><ASODOption><AppStoreOnVideo><OnClose>true<\\\/OnClose><OnDelayMs>2000<\\\/OnDelayMs><\\\/AppStoreOnVideo><AppStoreOnVideoEndCard><OnClose>true<\\\/OnClose><OnDelayMs>3000<\\\/OnDelayMs><\\\/AppStoreOnVideoEndCard><\\\/ASODOption><\\\/Extension><\\\/Extensions><\\\/InLine><\\\/Ad><\\\/VAST>"'
        over_ride_adm = over_ride_adm.replace("\\\\", "\\")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "VX_ENDCARD")
        assert_that(normal_replacements['VX_ENDCARD'], equal_to('true'))
        assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('16'))

    @allure.feature('programmatic Static Endcard')
    @allure.tag('basic')
    @allure.story('PBJ-5045 Add "close button delay control" for the last chance endcard (3rd page EC) for eDSP ads')
    @allure.description('Verify "EC_CLOSE_BUTTON_DELAY_SECONDS" in case of the vungle endcard as 2nd page endcard')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', ['HJKM6GM50916IMA0'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_vx_2nd_colse_button_delay_02(self, pub_app_id, placement, sdk_v, rtb_ids):
        """
        setting in dashboard:
        app level:
        allow_static_endcard: true
        adExperience.multiECCloseButtonDelay:11


        placement level:
        is_skippable: true
        """
        over_ride_adm = 'seatbid.0.bid.0.adm@"<VAST version=\\\"2.0\\\"><Ad><InLine><AdSystem><![CDATA[Bytedance]]><\\\/AdSystem><AdTitle><![CDATA[Bytedance]]><\\\/AdTitle><Impression><![CDATA[https:\\\/\\\/lf.snssdk.com\\\/api\\\/ad\\\/union\\\/show_event\\\/?req_id=5ec796d603e1e7c01267c88fu8791&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&source_type=1&pack_time=1590630440.65&pc=OMkaunPpDyKzZarhJKk3BmafV%2FjcG%2FID2AgSFwMkc6M%3D&ttdsp_price=${AUCTION_PRICE}]]><\\\/Impression><Creatives><Creative id=\\\"1665015151804428\\\"><Linear><Duration>00:00:46<\\\/Duration><TrackingEvents><Tracking event=\\\"start\\\"><![CDATA[https:\\\/\\\/is.snssdk.com\\\/api\\\/ad\\\/union\\\/event_report\\\/?event_type=4&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=0]]><\\\/Tracking><Tracking event=\\\"complete\\\"><![CDATA[https:\\\/\\\/is.snssdk.com\\\/api\\\/ad\\\/union\\\/event_report\\\/?event_type=6&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=27]]><\\\/Tracking><Tracking event=\\\"creativeView\\\"><![CDATA[http:\\\/\\\/app05.adfalcon.com\\\/E\\\/78c1743833b34d43991083f92bd5b392_0_b338d452-96f4-4d37-b6e1-d10de8271ff4?ev=creativeview]]><\\\/Tracking><\\\/TrackingEvents><VideoClicks><ClickThrough><![CDATA[https:\\\/\\\/events-dca.bidder.kayzen.io\\\/click?raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\\/ClickThrough><ClickTracking><![CDATA[https:\\\/\\\/lf.snssdk.com\\\/api\\\/ad\\\/union\\\/redirect\\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=1&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\\/ClickTracking><CustomClick id=\\\"ClickCoordinates-1\\\"><![CDATA[https:\\\/\\\/c2.gdt.qq.com\\\/gdt_mclick.fcg?viewid=!s6A4zH!POBbWj7ZQJudpxTBaTzOitZ8Zrj2cUWt!HRqifXlxVXVFYsSbE41QXp8NkVBskWi5Xu3It3wZDq05WhMsgfMLVxU41AQqVoe3wHYs6zZtEO_OtSDOHBiIm_Jn3xRWbR93zoDNI2kpylT7ltMreMCvonlVZ2Br0DCTf8SQOYklg8NNwTiMJCaTcC4xb7pIVEr5A5nkmccS3H9UpiMiJTk3eT_Yn57f4UxnMy9cxrAgVDosJFLJ6rXP6tZHCWVS3kSr0l5iRK1V956hwoVlIAVZCLcI!!qfcKzeS548ctKsM2Ps6ip5M9Cpx60&jtype=0&i=1&os=2&acttype=1&s={\\\"req_width\\\":\\\"__REQ_WIDTH__\\\",\\\"req_height\\\":\\\"__REQ_HEIGHT__\\\",\\\"width\\\":\\\"__WIDTH__\\\",\\\"height\\\":\\\"__HEIGHT__\\\",\\\"down_x\\\":\\\"__DOWN_X__\\\",\\\"down_y\\\":\\\"__DOWN_Y__\\\",\\\"up_x\\\":\\\"__UP_X__\\\",\\\"up_y\\\":\\\"__UP_Y__\\\"}&lpp=click_ext=eyJleHBfcGFyYW0iOiJjYXJyaWVyX2VuYWJsZToyIn0=&clklpp=__CLICK_LPP__&nxjp=1&cdnxj=1&xp=1&tl=1]]><\\\/CustomClick><CustomClick id=\\\"ClickCoordinates-2\\\"><![CDATA[http:\\\/\\\/link\\\/to\\\/customclick\\\/2]]><\\\/CustomClick><CustomClick id=\\\"customclick-3\\\"><![CDATA[http:\\\/\\\/link\\\/to\\\/customclick\\\/3]]><\\\/CustomClick><\\\/VideoClicks><MediaFiles><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[https:\\\/\\\/cdn-cn.vungle.cn\\\/zen\\\/497a5dead8498d62d7c65967729639f7-1280x720-Q2.mp4]]><\\\/MediaFile><MediaFile bitrate=\\\"372\\\" delivery=\\\"progressive\\\" height=\\\"360\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/mp4\\\" width=\\\"640\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/18\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/acao\\\/yes\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748513\\\/sparams\\\/id,itag,source,ctier,acao,ip,ipbits,expire\\\/signature\\\/484784AD6E9C1516EC07970AB978D11555654A9A.57EFB4F5F3CCE7F30CFBA1951E6434319300BE12\\\/key\\\/ck2\\\/file\\\/file.mp4 ]]><\\\/MediaFile><MediaFile bitrate=\\\"1879\\\" delivery=\\\"progressive\\\" height=\\\"720\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/22\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/acao\\\/yes\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748528\\\/sparams\\\/id,itag,source,ctier,acao,ip,ipbits,expire\\\/signature\\\/7136B1FF2CD283E5A90276E455C5F970B91A35FF.8E6707BA3249059D7BA09F6E3D59FF6BA1D78FE0\\\/key\\\/ck2\\\/file\\\/file.mp4 ]]><\\\/MediaFile><\\\/MediaFiles><\\\/Linear><\\\/Creative><\\\/Creatives><Description><![CDATA[Bytedance]]><\\\/Description><Survey><\\\/Survey><Extensions><Extension type=\\\"AdVerifications\\\"><AdVerifications><Verification vendor=\\\"moat.com-omsdkvungleinappvideo781943494431\\\"><JavaScriptResource apiFramework=\\\"omid\\\" browserOptional=\\\"true\\\"><![CDATA[https:\\\/\\\/z.moatads.com\\\/omsdkvungleinappvideo781943494431\\\/moatvideo.js]]><\\\/JavaScriptResource><VerificationParameters><![CDATA[{\\\"moatClientLevel1\\\":\\\"{{{app_id}}}\\\",\\\"moatClientLevel2\\\":\\\"{{{campaign_id}}}\\\",\\\"moatClientLevel3\\\":\\\"{{{creative_id}}}\\\",\\\"moatClientLevel4\\\":\\\"{{{placement_id}}}\\\",\\\"moatClientSlicer1\\\":\\\"{{{pub_app_id}}}\\\",\\\"moatClientLevel5\\\":\\\"{{{rtb_deal_id}}}\\\",\\\"moatClientLevel6\\\":\\\"{{{rtb_connection_id}}}\\\"}]]><\\\/VerificationParameters><\\\/Verification><\\\/AdVerifications><\\\/Extension><Extension type=\\\"Extra\\\"><CTA><![CDATA[Bytedance]]><\\\/CTA><SystemIcon><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/07c04164de3140d2cfe4bdd9812aef22~c1_0x0_q100.png]]><\\\/SystemIcon><FullStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/48c275deda9f2daa92acccf8218fc59f~c1_0x0_q100.jpeg]]><\\\/FullStar><HalfStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/b273598ab25fec09a467d2b895e3c53e~c1_0x0_q100.jpeg]]><\\\/HalfStar><EmptyStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/fedbae142b79804e383eed3f4d06e9d5~c1_0x0_q100.jpeg]]><\\\/EmptyStar><Review><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/297845a2690ec96bd1290a0a289ab373~c1_0x0_q100.jpeg]]><\\\/Review><MoPubCtaText><\\\/MoPubCtaText><\\\/Extension><Extension type=\\\"Vungle\\\"><ASODOption><AppStoreOnVideo><OnClose>true<\\\/OnClose><OnDelayMs>2000<\\\/OnDelayMs><\\\/AppStoreOnVideo><AppStoreOnVideoEndCard><OnClose>true<\\\/OnClose><OnDelayMs>3000<\\\/OnDelayMs><\\\/AppStoreOnVideoEndCard><\\\/ASODOption><\\\/Extension><\\\/Extensions><\\\/InLine><\\\/Ad><\\\/VAST>"'
        over_ride_adm = over_ride_adm.replace("\\\\", "\\")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "VX_ENDCARD")
        assert_that(normal_replacements['VX_ENDCARD'], equal_to('true'))
        assert_that(normal_replacements['EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to('11'))

    @allure.feature('programmatic Static Endcard')
    @allure.tag('basic')
    @allure.story('PBJ-5045 Add "close button delay control" for the last chance endcard (3rd page EC) for eDSP ads')
    @allure.description('Verify "EC_CLOSE_BUTTON_DELAY_SECONDS" in case of the vungle endcard as 3rd page endcard')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_crtype_attr_01])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_vx_3rd_colse_button_delay_01(self, pub_app_id, placement, sdk_v, rtb_ids):
        """
           setting in dashboard:
           app level:
           allow_skip_button: true
           allow_static_endcard: true
           static_ec_close_button_delay:25

           placement:
           supported_template_types:[
            "multi_page_fullscreen"
           ]
           NO static_ec_close_button_delay field.
           rtb:
           allow_skip_button: true


           bid:
              <VungleEndCard>
                <enable>true</enable>
            </VungleEndCard>

        """
        over_ride_adm = 'seatbid.0.bid.0.attr.0@13|||seatbid.0.bid.0.adm@"<VAST version=\\\"2.0\\\"><Ad><InLine><AdSystem><![CDATA[Bytedance]]><\\\/AdSystem><AdTitle><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\\/AdTitle><Impression><![CDATA[https:\\\/\\\/lf.snssdk.com\\\/api\\\/ad\\\/union\\\/show_event\\\/?req_id=5ec796d603e1e7c01267c88fu8791&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&source_type=1&pack_time=1590630440.65&pc=OMkaunPpDyKzZarhJKk3BmafV%2FjcG%2FID2AgSFwMkc6M%3D&ttdsp_price=${AUCTION_PRICE}]]><\\\/Impression><Creatives><Creative id=\\\"1665015151804428\\\"><Linear><Duration>00:00:46<\\\/Duration><TrackingEvents><Tracking event=\\\"start\\\"><![CDATA[https:\\\/\\\/is.snssdk.com\\\/api\\\/ad\\\/union\\\/event_report\\\/?event_type=4&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=0]]><\\\/Tracking><Tracking event=\\\"complete\\\"><![CDATA[https:\\\/\\\/is.snssdk.com\\\/api\\\/ad\\\/union\\\/event_report\\\/?event_type=6&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=27]]><\\\/Tracking><Tracking event=\\\"creativeView\\\"><![CDATA[http:\\\/\\\/app05.adfalcon.com\\\/E\\\/78c1743833b34d43991083f92bd5b392_0_b338d452-96f4-4d37-b6e1-d10de8271ff4?ev=creativeview]]><\\\/Tracking><\\\/TrackingEvents><VideoClicks><ClickThrough><![CDATA[https:\\\/\\\/events-dca.bidder.kayzen.io\\\/click?raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\\/ClickThrough><ClickTracking><![CDATA[https:\\\/\\\/lf.snssdk.com\\\/api\\\/ad\\\/union\\\/redirect\\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=1&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\\/ClickTracking><CustomClick id=\\\"ClickCoordinates-1\\\"><![CDATA[https:\\\/\\\/c2.gdt.qq.com\\\/gdt_mclick.fcg?viewid=!s6A4zH!POBbWj7ZQJudpxTBaTzOitZ8Zrj2cUWt!HRqifXlxVXVFYsSbE41QXp8NkVBskWi5Xu3It3wZDq05WhMsgfMLVxU41AQqVoe3wHYs6zZtEO_OtSDOHBiIm_Jn3xRWbR93zoDNI2kpylT7ltMreMCvonlVZ2Br0DCTf8SQOYklg8NNwTiMJCaTcC4xb7pIVEr5A5nkmccS3H9UpiMiJTk3eT_Yn57f4UxnMy9cxrAgVDosJFLJ6rXP6tZHCWVS3kSr0l5iRK1V956hwoVlIAVZCLcI!!qfcKzeS548ctKsM2Ps6ip5M9Cpx60&jtype=0&i=1&os=2&acttype=1&s={\\\"req_width\\\":\\\"__REQ_WIDTH__\\\",\\\"req_height\\\":\\\"__REQ_HEIGHT__\\\",\\\"width\\\":\\\"__WIDTH__\\\",\\\"height\\\":\\\"__HEIGHT__\\\",\\\"down_x\\\":\\\"__DOWN_X__\\\",\\\"down_y\\\":\\\"__DOWN_Y__\\\",\\\"up_x\\\":\\\"__UP_X__\\\",\\\"up_y\\\":\\\"__UP_Y__\\\"}&lpp=click_ext=eyJleHBfcGFyYW0iOiJjYXJyaWVyX2VuYWJsZToyIn0=&clklpp=__CLICK_LPP__&nxjp=1&cdnxj=1&xp=1&tl=1]]><\\\/CustomClick><CustomClick id=\\\"ClickCoordinates-2\\\"><![CDATA[http:\\\/\\\/link\\\/to\\\/customclick\\\/2]]><\\\/CustomClick><CustomClick id=\\\"customclick-3\\\"><![CDATA[http:\\\/\\\/link\\\/to\\\/customclick\\\/3]]><\\\/CustomClick><\\\/VideoClicks><MediaFiles><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[ asdjfklajsd;fkja;sdlkfjklasdjfklasdjfkl.mp4 ]]><\\\/MediaFile><MediaFile bitrate=\\\"206\\\" delivery=\\\"progressive\\\" height=\\\"180\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/3gpp\\\" width=\\\"320\\\"><![CDATA[ test\\\/jsldfjlksdfjk.mp4 ]]><\\\/MediaFile><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[ v3-ad.ixigua.com\\\/kghkhk\\\/toutiao123werwerew.abc ]]><\\\/MediaFile><MediaFile bitrate=\\\"56\\\" delivery=\\\"progressive\\\" height=\\\"144\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/3gpp\\\" width=\\\"176\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/17\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748511\\\/sparams\\\/id,itag,source,ctier,ip,ipbits,expire\\\/signature\\\/8044BE9E3E1793FF36C03998BA13848E7C845ABE.75B6CAFBF57F6F96C78BDFCEB9653E601FD7E8D8\\\/key\\\/ck2\\\/file\\\/file.3gpp ]]><\\\/MediaFile><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[https:\\\/\\\/v3-ad.ixigua.com\\\/kghkhk\\\/toutiao123]]><\\\/MediaFile><MediaFile bitrate=\\\"206\\\" delivery=\\\"progressive\\\" height=\\\"180\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/3gpp\\\" width=\\\"320\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/36\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748512\\\/sparams\\\/id,itag,source,ctier,ip,ipbits,expire\\\/signature\\\/29EC5A3574F0873D71FF75DEA54B89FD30A0D0B1.82B0C3EBBBAF7046A8DFBF3D94AAD9FC69C5C9A4\\\/key\\\/ck2\\\/file\\\/file.3gpp ]]><\\\/MediaFile><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[https:\\\/\\\/cdn-cn.vungle.cn\\\/zen\\\/497a5dead8498d62d7c65967729639f7-1280x720-Q2.mp4]]><\\\/MediaFile><MediaFile bitrate=\\\"372\\\" delivery=\\\"progressive\\\" height=\\\"360\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/mp4\\\" width=\\\"640\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/18\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/acao\\\/yes\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748513\\\/sparams\\\/id,itag,source,ctier,acao,ip,ipbits,expire\\\/signature\\\/484784AD6E9C1516EC07970AB978D11555654A9A.57EFB4F5F3CCE7F30CFBA1951E6434319300BE12\\\/key\\\/ck2\\\/file\\\/file.mp4 ]]><\\\/MediaFile><MediaFile bitrate=\\\"1879\\\" delivery=\\\"progressive\\\" height=\\\"720\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/22\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/acao\\\/yes\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748528\\\/sparams\\\/id,itag,source,ctier,acao,ip,ipbits,expire\\\/signature\\\/7136B1FF2CD283E5A90276E455C5F970B91A35FF.8E6707BA3249059D7BA09F6E3D59FF6BA1D78FE0\\\/key\\\/ck2\\\/file\\\/file.mp4 ]]><\\\/MediaFile><\\\/MediaFiles><\\\/Linear><\\\/Creative><Creative><CompanionAds><Companion width=\\\"480\\\" height=\\\"320\\\"><HTMLResource><![CDATA[<div style=\\\"position:absolute;top:0;bottom:0;left:0;right:0;\\\"><meta charset=\\\"utf-8\\\"\\\/><meta name=\\\"viewport\\\" content=\\\"width=device-width,initial-scale=1,user-scalable=no\\\"\\\/><a id=\\\"exchange-ping-url\\\" href=\\\"https:\\\/\\\/cdn.liftoff.io\\\/tracking_pixel.gif\\\" style=\\\"display:none\\\"><\\\/a><script>window.LIFTOFF_START_TS = Date.now()<\\\/script><script src=\\\"https:\\\/\\\/cdn.liftoff.io\\\/resources\\\/polyfills-33c384a010d661c2a64d.js\\\"><\\\/script><div id=\\\"tracking-tag-holder\\\" style=\\\"display:none\\\"><\\\/div><script src=\\\"https:\\\/\\\/cdn.liftoff.io\\\/resources\\\/outer_env-aae1d794a14769f5efcc.js\\\"><\\\/script><div id=\\\"liftoff-snippet\\\"><\\\/div><script>LiftoffOuterEnv.init({inProd: true,containerEl: document.getElementById(\\\"liftoff-snippet\\\"),envData: JSON.parse(decodeURIComponent(\'{\\\"clickURLs\\\":{\\\"clickthroughURL\\\":{\\\"url\\\":\\\"https:\\\/\\\/play.google.com\\\/store\\\/apps\\\/details%3Fid=com.playrix.township\\\",\\\"type\\\":2},\\\"clickTrackingURLs\\\":%5B{\\\"url\\\":\\\"https:\\\/\\\/click.liftoff.io\\\/v1\\\/campaign_click\\\/Mg7kXlNeI6IpbPMmKzZY_ztMYM6NO1OeUtL7NsADF-hcIl_fVATEOtZ5jelfNO7I3TKARpSfHHHxEXfDLJalv9ui50FzdKTT3J15quufe6oxCz-RHA4LAZH70RhIJ6E29NjJFl0lG_8JKgaH29DOceobtRV7Um0DSfKEnyyGHg_P87C3QOyQLZD4oIlLSpdfr0BBoUvH_3yIq9WNf6VG6eltwUSDd_ONKwaeEjbX0pCLDTr9R-HIfxpmb4LyTx0otoP6tRnS-QrE0tYnlFpMyjcHaArwt2f6_48fwWEdREjOVek8RDeptq7HNiOnRVLbbCdWXb9F1isw9jjphxlFEZZOhGU10iRpylSmKZw7WmPt2EVhcdsy_KWhe-KkNXWm-O8PUzqZNxKoM9-z5wgbZmJrOdgq0IHbbY-iQQVr640w3mPnnoGqGZBAj8PS2CLGNDCd8oCFe0PuQpsykAJ4ZeUwrq3S7TOvKqpd5_Bcpb1_pXitJ7UBh7l4yeb5gl9udGXyE02dysrtz2BICk4Rvopw2FwPPXWlEWsOF-lkx2QYQ9Pu2Y5MYa62ow0qqhcaogU6uj0ghqKqjG_mfw%3Fvast_el=3\\\",\\\"type\\\":1}%5D},\\\"costModel\\\":null,\\\"pinpointURL\\\":\\\"https:\\\/\\\/play.google.com\\\/store\\\/apps\\\/details%3Fid=com.playrix.township\\\",\\\"isReengagement\\\":false,\\\"impression\\\":{\\\"auctionID\\\":\\\"61516e15294ecded58f89c8e\\\",\\\"isRewarded\\\":true},\\\"loggingConfig\\\":{\\\"enableHTMLReturn\\\":false,\\\"eventTrackingParam\\\":\\\"c9dfb5CN3VBxIYNjE1MTZlMTUyOTRlY2RlZDU4Zjg5YzhlGIiE2LDCLyAYKPuCDTCbCzoiY29tLm9zLmZhbGNvbi5ib2IyLmFkdmVudHVyZS53b3JsZEIaY2xpY2std2F0ZXJmYWxsLXYyLWNvbnRyb2xCG3Zhc3QtaHRtbC1lbmRzY3JlZW4tY29udHJvbEIcaW9zLWh0bWwtbWV0YS1oZWFkZXItY29udHJvbEIbY3NwLXNyY2RvYy1wcmlvcml0eS1jb250cm9sQhdhcHAtc3RvcmUtbW9kYWwtY29udHJvbEoKNDFjMjE4YjEzNFADWgNJRE5gAmgEcg5hcC1ub3J0aGVhc3QtMYABGJIBAmlkmAECoQEzMzMzMzOzP6oBCDE2NDB4ODEwsgEJQWR2ZW50dXJlugEcQm9iJ3MgV29ybGQgMiAtIFJ1bm5pbmcgZ2FtZcIBGXZhc3QtY2RiNDU5ZDNjNjViMTdkODdlMGLKAQIBAtIBAA\\\",\\\"htmlReturnDelay\\\":\\\"5000\\\",\\\"enableLogging\\\":true,\\\"loggingEndpoint\\\":\\\"https:\\\/\\\/adexp.liftoff.io\\\"},\\\"clickConfig\\\":{\\\"clickthroughURL\\\":{\\\"url\\\":\\\"https:\\\/\\\/play.google.com\\\/store\\\/apps\\\/details%3Fid=com.playrix.township\\\",\\\"type\\\":2},\\\"clickTrackingURLs\\\":%5B{\\\"url\\\":\\\"https:\\\/\\\/click.liftoff.io\\\/v1\\\/campaign_click\\\/Mg7kXlNeI6IpbPMmKzZY_ztMYM6NO1OeUtL7NsADF-hcIl_fVATEOtZ5jelfNO7I3TKARpSfHHHxEXfDLJalv9ui50FzdKTT3J15quufe6oxCz-RHA4LAZH70RhIJ6E29NjJFl0lG_8JKgaH29DOceobtRV7Um0DSfKEnyyGHg_P87C3QOyQLZD4oIlLSpdfr0BBoUvH_3yIq9WNf6VG6eltwUSDd_ONKwaeEjbX0pCLDTr9R-HIfxpmb4LyTx0otoP6tRnS-QrE0tYnlFpMyjcHaArwt2f6_48fwWEdREjOVek8RDeptq7HNiOnRVLbbCdWXb9F1isw9jjphxlFEZZOhGU10iRpylSmKZw7WmPt2EVhcdsy_KWhe-KkNXWm-O8PUzqZNxKoM9-z5wgbZmJrOdgq0IHbbY-iQQVr640w3mPnnoGqGZBAj8PS2CLGNDCd8oCFe0PuQpsykAJ4ZeUwrq3S7TOvKqpd5_Bcpb1_pXitJ7UBh7l4yeb5gl9udGXyE02dysrtz2BICk4Rvopw2FwPPXWlEWsOF-lkx2QYQ9Pu2Y5MYa62ow0qqhcaogU6uj0ghqKqjG_mfw%3Fvast_el=3\\\",\\\"type\\\":1}%5D},\\\"cdnURL\\\":\\\"https:\\\/\\\/cdn.liftoff.io\\\",\\\"geo\\\":{\\\"latitude\\\":-7.2484,\\\"longitude\\\":112.7419},\\\"creative\\\":{\\\"id\\\":213371,\\\"width\\\":480,\\\"height\\\":320,\\\"name\\\":\\\"%28image211%29480x320_ts_video661v1_nst_en_30s_20mb_options_playable124\\\",\\\"params\\\":%5B%5D},\\\"abTests\\\":%5B\\\"click-waterfall-v2-control\\\",\\\"vast-html-endscreen-control\\\",\\\"ios-html-meta-header-control\\\",\\\"csp-srcdoc-priority-control\\\",\\\"app-store-modal-control\\\"%5D,\\\"app\\\":{\\\"id\\\":\\\"com.os.falcon.bob2.adventure.world\\\",\\\"name\\\":\\\"Bob%27s World 2 - Running game\\\"},\\\"campaign\\\":{\\\"id\\\":15373,\\\"name\\\":\\\"TS_GP_AP_Low\\\",\\\"params\\\":%5B%5D},\\\"creativePolicy\\\":{\\\"animationDurationLimit\\\":0,\\\"audioPolicy\\\":\\\"always-mute\\\",\\\"russianAgeRating\\\":null,\\\"removeAdWrapper\\\":false,\\\"showAdChoices\\\":false,\\\"addBorder\\\":false,\\\"useCustomClose\\\":false,\\\"closeDelay\\\":5,\\\"blockNotifications\\\":false,\\\"showChineseWatermark\\\":false,\\\"blockStrobing\\\":false},\\\"device\\\":{\\\"googleAID\\\":\\\"aa9f2aa4-845d-4bfe-bc6b-9150e1b1551d\\\",\\\"connectionType\\\":3,\\\"googleAIDSHA1\\\":\\\"b34af918dd77461b498a5af0e54d84895de14ed8\\\",\\\"ip\\\":\\\"112.215.237.195\\\",\\\"idfaSHA1\\\":null,\\\"androidIDMD5\\\":null,\\\"idfa\\\":null,\\\"normalizedLanguage\\\":\\\"id\\\",\\\"osVersion\\\":\\\"11\\\",\\\"idfaMD5\\\":null,\\\"androidIDSHA1\\\":null,\\\"androidID\\\":null,\\\"platform\\\":\\\"android\\\",\\\"model\\\":\\\"\\\"},\\\"trackingToken\\\":\\\"v.2_g.125661_a.61516e15294ecded58f89c8e_c.24_t.ua_u.b34af918dd77461b\\\",\\\"exchange\\\":\\\"vungle\\\",\\\"isStaffDevice\\\":false,\\\"platform\\\":\\\"android\\\"}\')),scriptSrcURLs: [\\\"https:\\\/\\\/cdn.liftoff.io\\\/resources\\\/polyfills-33c384a010d661c2a64d.js\\\",\\\"https:\\\/\\\/cdn.liftoff.io\\\/resources\\\/inner_env-bfa56fb84006156f82f7.js\\\"],rootURL: \\\"https:\\\/\\\/cdn.liftoff.io\\\/customers\\\/753\\\/creatives\\\/205394\\\/\\\",html: \'%3C%21DOCTYPE html%3E%3Chtml%3E%3Chead%3E%3Cmeta charset=\\\"utf-8\\\"%3E%3Ctitle%3EPlayable%3C\\\/title%3E%3Cmeta name=\\\"viewport\\\" content=\\\"width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover\\\"%3E%3C\\\/head%3E%3Cbody%3E%3Cscript type=\\\"text\\\/javascript\\\"%3Ewindow.apiName=\\\"liftoff\\\"%3Bwindow.playableEnv={\\\"lang\\\":\\\"en\\\",\\\"apiName\\\":\\\"liftoff\\\",\\\"nameGameAbbr\\\":\\\"ts\\\",\\\"params\\\":{\\\"showInstallButton\\\":true}}%3C\\\/script%3E%3Cdiv id=\\\"styles-container\\\"%3E%3C\\\/div%3E%3Cdiv id=\\\"scripts-container\\\"%3E%3C\\\/div%3E%3Cscript type=\\\"text\\\/javascript\\\"%3Ewindow.addEventListener%28\\\"load\\\",function%28%29{var is_ready_app,is_ready_timer,ROOT_URL=\\\"\\\"%3B\\\"undefined\\\"%21=typeof LIFTOFF_ROOT_URL%26%26%28ROOT_URL=LIFTOFF_ROOT_URL%29%3Bvar name,cb,style,counter=0%3Bfunction next%28%29{loader.create%28%29,setTimeout%28function%28%29{is_ready_timer=%210,init%28%29},1e3%29,js%28\\\"app.js\\\",function%28%29{is_ready_app=%210,init%28%29}%29}function init%28%29{is_ready_timer%26%26is_ready_app%26%26%28\\\"undefined\\\"%21=typeof superApp%3FsuperApp.init%28%29:initGame%28%29,\\\"undefined\\\"%21=typeof loader%26%26loader.clear%28%29%29}function js%28name,cb%29{var script=document.createElement%28\\\"script\\\"%29%3Bscript.src=ROOT_URL+name,document.getElementById%28\\\"scripts-container\\\"%29.appendChild%28script%29,script.onload=function%28%29{cb%26%26cb%28%29}}js%28\\\"loader.js\\\",function%28%29{2==++counter%26%26next%28%29}%29,name=\\\"styles.css\\\",cb=function%28%29{2==++counter%26%26next%28%29},%28style=document.createElement%28\\\"link\\\"%29%29.href=ROOT_URL+name,style.type=\\\"text\\\/css\\\",style.rel=\\\"stylesheet\\\",style.media=\\\"screen,print\\\",document.getElementById%28\\\"styles-container\\\"%29.appendChild%28style%29,style.onload=function%28%29{cb%26%26cb%28%29},window.clickInstall=function%28%29{window.open%28window._LIFTOFF_ENV.pinpointURL,\\\"_blank\\\"%29}}%29%3B%3C\\\/script%3E%3C\\\/body%3E%3C\\\/html%3E\',externalHtmlURL: null,});<\\\/script><\\\/div>]]><\\\/HTMLResource><TrackingEvents><Tracking event=\\\"creativeView\\\"><![CDATA[https:\\\/\\\/adexp.liftoff.io\\\/event\\\/vast\\\/htmlEndscreenView\\\/c9dfb5CN3VBxIYNjE1MTZlMTUyOTRlY2RlZDU4Zjg5YzhlGIiE2LDCLyAYKPuCDTCbCzoiY29tLm9zLmZhbGNvbi5ib2IyLmFkdmVudHVyZS53b3JsZEIaY2xpY2std2F0ZXJmYWxsLXYyLWNvbnRyb2xCG3Zhc3QtaHRtbC1lbmRzY3JlZW4tY29udHJvbEIcaW9zLWh0bWwtbWV0YS1oZWFkZXItY29udHJvbEIbY3NwLXNyY2RvYy1wcmlvcml0eS1jb250cm9sQhdhcHAtc3RvcmUtbW9kYWwtY29udHJvbEoKNDFjMjE4YjEzNFADWgNJRE5gAmgEcg5hcC1ub3J0aGVhc3QtMYABGJIBAmlkmAECoQEzMzMzMzOzP6oBCDE2NDB4ODEwsgEJQWR2ZW50dXJlugEcQm9iJ3MgV29ybGQgMiAtIFJ1bm5pbmcgZ2FtZcIBGXZhc3QtY2RiNDU5ZDNjNjViMTdkODdlMGLKAQIBAtIBAA?playhead=[CONTENTPLAYHEAD]&sr=1]]><\\\/Tracking><\\\/TrackingEvents><\\\/Companion><\\\/CompanionAds><\\\/Creative><\\\/Creatives><Description><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\\/Description><Survey><\\\/Survey><Extensions><Extension type=\\\"AdVerifications\\\"><AdVerifications><Verification vendor=\\\"moat.com-omsdkvungleinappvideo781943494431\\\"><JavaScriptResource apiFramework=\\\"omid\\\" browserOptional=\\\"true\\\"><![CDATA[https:\\\/\\\/z.moatads.com\\\/omsdkvungleinappvideo781943494431\\\/moatvideo.js]]><\\\/JavaScriptResource><VerificationParameters><![CDATA[{\\\"moatClientLevel1\\\":\\\"{{{app_id}}}\\\",\\\"moatClientLevel2\\\":\\\"{{{campaign_id}}}\\\",\\\"moatClientLevel3\\\":\\\"{{{creative_id}}}\\\",\\\"moatClientLevel4\\\":\\\"{{{placement_id}}}\\\",\\\"moatClientSlicer1\\\":\\\"{{{pub_app_id}}}\\\",\\\"moatClientLevel5\\\":\\\"{{{rtb_deal_id}}}\\\",\\\"moatClientLevel6\\\":\\\"{{{rtb_connection_id}}}\\\"}]]><\\\/VerificationParameters><\\\/Verification><\\\/AdVerifications><\\\/Extension><Extension type=\\\"Extra\\\"><CTA><![CDATA[\\u70B9\\u51FB\\u4E0B\\u8F7D]]><\\\/CTA><SystemIcon><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/07c04164de3140d2cfe4bdd9812aef22~c1_0x0_q100.png]]><\\\/SystemIcon><FullStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/48c275deda9f2daa92acccf8218fc59f~c1_0x0_q100.jpeg]]><\\\/FullStar><HalfStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/b273598ab25fec09a467d2b895e3c53e~c1_0x0_q100.jpeg]]><\\\/HalfStar><EmptyStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/fedbae142b79804e383eed3f4d06e9d5~c1_0x0_q100.jpeg]]><\\\/EmptyStar><Review><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/297845a2690ec96bd1290a0a289ab373~c1_0x0_q100.jpeg]]><\\\/Review><MoPubCtaText><\\\/MoPubCtaText><\\\/Extension><Extension type=\\\"Vungle\\\"><ASODOption><VungleEndCard><enable>true<\\/enable><\\/VungleEndCard><AppStoreOnVideo><OnClose>true<\\\/OnClose><OnDelayMs>2000<\\\/OnDelayMs><\\\/AppStoreOnVideo><AppStoreOnVideoEndCard><OnClose>true<\\\/OnClose><OnDelayMs>3000<\\\/OnDelayMs><\\\/AppStoreOnVideoEndCard><\\\/ASODOption><\\\/Extension><\\\/Extensions><\\\/InLine><\\\/Ad><\\\/VAST>"'
        over_ride_adm = over_ride_adm.replace("\\\\", "\\")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "VX_ENDCARD")
        assert_that(normal_replacements["VX_ENDCARD"], equal_to('true'))
        assert_keys_not_exist(normal_replacements, 'STATIC_EC_CLOSE_BUTTON_DELAY_SECONDS')

    @allure.feature('programmatic Static Endcard')
    @allure.tag('basic')
    @allure.story('PBJ-5045 Add "close button delay control" for the last chance endcard (3rd page EC) for eDSP ads')
    @allure.description('Verify "EC_CLOSE_BUTTON_DELAY_SECONDS" in case of the vungle endcard as 3rd page endcard')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_crtype_attr_02])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_vx_3rd_colse_button_delay_02(self, pub_app_id, placement, sdk_v, rtb_ids):
        """
           setting in dashboard:
           app level:
           allow_skip_button: true
           allow_static_endcard: true
           static_ec_close_button_delay:25

           placement:
           supported_template_types:[
            "multi_page_fullscreen"
           ]
           static_ec_close_button_delay:6.
           rtb:
           allow_skip_button: true


           bid:
              <VungleEndCard>
                <enable>true</enable>
            </VungleEndCard>

        """
        over_ride_adm = 'seatbid.0.bid.0.attr.0@13|||seatbid.0.bid.0.adm@"<VAST version=\\\"2.0\\\"><Ad><InLine><AdSystem><![CDATA[Bytedance]]><\\\/AdSystem><AdTitle><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\\/AdTitle><Impression><![CDATA[https:\\\/\\\/lf.snssdk.com\\\/api\\\/ad\\\/union\\\/show_event\\\/?req_id=5ec796d603e1e7c01267c88fu8791&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&source_type=1&pack_time=1590630440.65&pc=OMkaunPpDyKzZarhJKk3BmafV%2FjcG%2FID2AgSFwMkc6M%3D&ttdsp_price=${AUCTION_PRICE}]]><\\\/Impression><Creatives><Creative id=\\\"1665015151804428\\\"><Linear><Duration>00:00:46<\\\/Duration><TrackingEvents><Tracking event=\\\"start\\\"><![CDATA[https:\\\/\\\/is.snssdk.com\\\/api\\\/ad\\\/union\\\/event_report\\\/?event_type=4&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=0]]><\\\/Tracking><Tracking event=\\\"complete\\\"><![CDATA[https:\\\/\\\/is.snssdk.com\\\/api\\\/ad\\\/union\\\/event_report\\\/?event_type=6&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=27]]><\\\/Tracking><Tracking event=\\\"creativeView\\\"><![CDATA[http:\\\/\\\/app05.adfalcon.com\\\/E\\\/78c1743833b34d43991083f92bd5b392_0_b338d452-96f4-4d37-b6e1-d10de8271ff4?ev=creativeview]]><\\\/Tracking><\\\/TrackingEvents><VideoClicks><ClickThrough><![CDATA[https:\\\/\\\/events-dca.bidder.kayzen.io\\\/click?raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\\/ClickThrough><ClickTracking><![CDATA[https:\\\/\\\/lf.snssdk.com\\\/api\\\/ad\\\/union\\\/redirect\\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=1&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\\/ClickTracking><CustomClick id=\\\"ClickCoordinates-1\\\"><![CDATA[https:\\\/\\\/c2.gdt.qq.com\\\/gdt_mclick.fcg?viewid=!s6A4zH!POBbWj7ZQJudpxTBaTzOitZ8Zrj2cUWt!HRqifXlxVXVFYsSbE41QXp8NkVBskWi5Xu3It3wZDq05WhMsgfMLVxU41AQqVoe3wHYs6zZtEO_OtSDOHBiIm_Jn3xRWbR93zoDNI2kpylT7ltMreMCvonlVZ2Br0DCTf8SQOYklg8NNwTiMJCaTcC4xb7pIVEr5A5nkmccS3H9UpiMiJTk3eT_Yn57f4UxnMy9cxrAgVDosJFLJ6rXP6tZHCWVS3kSr0l5iRK1V956hwoVlIAVZCLcI!!qfcKzeS548ctKsM2Ps6ip5M9Cpx60&jtype=0&i=1&os=2&acttype=1&s={\\\"req_width\\\":\\\"__REQ_WIDTH__\\\",\\\"req_height\\\":\\\"__REQ_HEIGHT__\\\",\\\"width\\\":\\\"__WIDTH__\\\",\\\"height\\\":\\\"__HEIGHT__\\\",\\\"down_x\\\":\\\"__DOWN_X__\\\",\\\"down_y\\\":\\\"__DOWN_Y__\\\",\\\"up_x\\\":\\\"__UP_X__\\\",\\\"up_y\\\":\\\"__UP_Y__\\\"}&lpp=click_ext=eyJleHBfcGFyYW0iOiJjYXJyaWVyX2VuYWJsZToyIn0=&clklpp=__CLICK_LPP__&nxjp=1&cdnxj=1&xp=1&tl=1]]><\\\/CustomClick><CustomClick id=\\\"ClickCoordinates-2\\\"><![CDATA[http:\\\/\\\/link\\\/to\\\/customclick\\\/2]]><\\\/CustomClick><CustomClick id=\\\"customclick-3\\\"><![CDATA[http:\\\/\\\/link\\\/to\\\/customclick\\\/3]]><\\\/CustomClick><\\\/VideoClicks><MediaFiles><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[ asdjfklajsd;fkja;sdlkfjklasdjfklasdjfkl.mp4 ]]><\\\/MediaFile><MediaFile bitrate=\\\"206\\\" delivery=\\\"progressive\\\" height=\\\"180\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/3gpp\\\" width=\\\"320\\\"><![CDATA[ test\\\/jsldfjlksdfjk.mp4 ]]><\\\/MediaFile><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[ v3-ad.ixigua.com\\\/kghkhk\\\/toutiao123werwerew.abc ]]><\\\/MediaFile><MediaFile bitrate=\\\"56\\\" delivery=\\\"progressive\\\" height=\\\"144\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/3gpp\\\" width=\\\"176\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/17\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748511\\\/sparams\\\/id,itag,source,ctier,ip,ipbits,expire\\\/signature\\\/8044BE9E3E1793FF36C03998BA13848E7C845ABE.75B6CAFBF57F6F96C78BDFCEB9653E601FD7E8D8\\\/key\\\/ck2\\\/file\\\/file.3gpp ]]><\\\/MediaFile><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[https:\\\/\\\/v3-ad.ixigua.com\\\/kghkhk\\\/toutiao123]]><\\\/MediaFile><MediaFile bitrate=\\\"206\\\" delivery=\\\"progressive\\\" height=\\\"180\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/3gpp\\\" width=\\\"320\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/36\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748512\\\/sparams\\\/id,itag,source,ctier,ip,ipbits,expire\\\/signature\\\/29EC5A3574F0873D71FF75DEA54B89FD30A0D0B1.82B0C3EBBBAF7046A8DFBF3D94AAD9FC69C5C9A4\\\/key\\\/ck2\\\/file\\\/file.3gpp ]]><\\\/MediaFile><MediaFile delivery=\\\"progressive\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\" height=\\\"720\\\"><![CDATA[https:\\\/\\\/cdn-cn.vungle.cn\\\/zen\\\/497a5dead8498d62d7c65967729639f7-1280x720-Q2.mp4]]><\\\/MediaFile><MediaFile bitrate=\\\"372\\\" delivery=\\\"progressive\\\" height=\\\"360\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/mp4\\\" width=\\\"640\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/18\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/acao\\\/yes\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748513\\\/sparams\\\/id,itag,source,ctier,acao,ip,ipbits,expire\\\/signature\\\/484784AD6E9C1516EC07970AB978D11555654A9A.57EFB4F5F3CCE7F30CFBA1951E6434319300BE12\\\/key\\\/ck2\\\/file\\\/file.mp4 ]]><\\\/MediaFile><MediaFile bitrate=\\\"1879\\\" delivery=\\\"progressive\\\" height=\\\"720\\\" maintainAspectRatio=\\\"false\\\" scalable=\\\"false\\\" type=\\\"video\\\/mp4\\\" width=\\\"1280\\\"><![CDATA[ https:\\\/\\\/gcdn.2mdn.net\\\/videoplayback\\\/id\\\/1fe270df6ccb6f2c\\\/itag\\\/22\\\/source\\\/doubleclick_dmm\\\/ctier\\\/L\\\/acao\\\/yes\\\/ip\\\/0.0.0.0\\\/ipbits\\\/0\\\/expire\\\/3738748528\\\/sparams\\\/id,itag,source,ctier,acao,ip,ipbits,expire\\\/signature\\\/7136B1FF2CD283E5A90276E455C5F970B91A35FF.8E6707BA3249059D7BA09F6E3D59FF6BA1D78FE0\\\/key\\\/ck2\\\/file\\\/file.mp4 ]]><\\\/MediaFile><\\\/MediaFiles><\\\/Linear><\\\/Creative><Creative><CompanionAds><Companion width=\\\"480\\\" height=\\\"320\\\"><HTMLResource><![CDATA[<div style=\\\"position:absolute;top:0;bottom:0;left:0;right:0;\\\"><meta charset=\\\"utf-8\\\"\\\/><meta name=\\\"viewport\\\" content=\\\"width=device-width,initial-scale=1,user-scalable=no\\\"\\\/><a id=\\\"exchange-ping-url\\\" href=\\\"https:\\\/\\\/cdn.liftoff.io\\\/tracking_pixel.gif\\\" style=\\\"display:none\\\"><\\\/a><script>window.LIFTOFF_START_TS = Date.now()<\\\/script><script src=\\\"https:\\\/\\\/cdn.liftoff.io\\\/resources\\\/polyfills-33c384a010d661c2a64d.js\\\"><\\\/script><div id=\\\"tracking-tag-holder\\\" style=\\\"display:none\\\"><\\\/div><script src=\\\"https:\\\/\\\/cdn.liftoff.io\\\/resources\\\/outer_env-aae1d794a14769f5efcc.js\\\"><\\\/script><div id=\\\"liftoff-snippet\\\"><\\\/div><script>LiftoffOuterEnv.init({inProd: true,containerEl: document.getElementById(\\\"liftoff-snippet\\\"),envData: JSON.parse(decodeURIComponent(\'{\\\"clickURLs\\\":{\\\"clickthroughURL\\\":{\\\"url\\\":\\\"https:\\\/\\\/play.google.com\\\/store\\\/apps\\\/details%3Fid=com.playrix.township\\\",\\\"type\\\":2},\\\"clickTrackingURLs\\\":%5B{\\\"url\\\":\\\"https:\\\/\\\/click.liftoff.io\\\/v1\\\/campaign_click\\\/Mg7kXlNeI6IpbPMmKzZY_ztMYM6NO1OeUtL7NsADF-hcIl_fVATEOtZ5jelfNO7I3TKARpSfHHHxEXfDLJalv9ui50FzdKTT3J15quufe6oxCz-RHA4LAZH70RhIJ6E29NjJFl0lG_8JKgaH29DOceobtRV7Um0DSfKEnyyGHg_P87C3QOyQLZD4oIlLSpdfr0BBoUvH_3yIq9WNf6VG6eltwUSDd_ONKwaeEjbX0pCLDTr9R-HIfxpmb4LyTx0otoP6tRnS-QrE0tYnlFpMyjcHaArwt2f6_48fwWEdREjOVek8RDeptq7HNiOnRVLbbCdWXb9F1isw9jjphxlFEZZOhGU10iRpylSmKZw7WmPt2EVhcdsy_KWhe-KkNXWm-O8PUzqZNxKoM9-z5wgbZmJrOdgq0IHbbY-iQQVr640w3mPnnoGqGZBAj8PS2CLGNDCd8oCFe0PuQpsykAJ4ZeUwrq3S7TOvKqpd5_Bcpb1_pXitJ7UBh7l4yeb5gl9udGXyE02dysrtz2BICk4Rvopw2FwPPXWlEWsOF-lkx2QYQ9Pu2Y5MYa62ow0qqhcaogU6uj0ghqKqjG_mfw%3Fvast_el=3\\\",\\\"type\\\":1}%5D},\\\"costModel\\\":null,\\\"pinpointURL\\\":\\\"https:\\\/\\\/play.google.com\\\/store\\\/apps\\\/details%3Fid=com.playrix.township\\\",\\\"isReengagement\\\":false,\\\"impression\\\":{\\\"auctionID\\\":\\\"61516e15294ecded58f89c8e\\\",\\\"isRewarded\\\":true},\\\"loggingConfig\\\":{\\\"enableHTMLReturn\\\":false,\\\"eventTrackingParam\\\":\\\"c9dfb5CN3VBxIYNjE1MTZlMTUyOTRlY2RlZDU4Zjg5YzhlGIiE2LDCLyAYKPuCDTCbCzoiY29tLm9zLmZhbGNvbi5ib2IyLmFkdmVudHVyZS53b3JsZEIaY2xpY2std2F0ZXJmYWxsLXYyLWNvbnRyb2xCG3Zhc3QtaHRtbC1lbmRzY3JlZW4tY29udHJvbEIcaW9zLWh0bWwtbWV0YS1oZWFkZXItY29udHJvbEIbY3NwLXNyY2RvYy1wcmlvcml0eS1jb250cm9sQhdhcHAtc3RvcmUtbW9kYWwtY29udHJvbEoKNDFjMjE4YjEzNFADWgNJRE5gAmgEcg5hcC1ub3J0aGVhc3QtMYABGJIBAmlkmAECoQEzMzMzMzOzP6oBCDE2NDB4ODEwsgEJQWR2ZW50dXJlugEcQm9iJ3MgV29ybGQgMiAtIFJ1bm5pbmcgZ2FtZcIBGXZhc3QtY2RiNDU5ZDNjNjViMTdkODdlMGLKAQIBAtIBAA\\\",\\\"htmlReturnDelay\\\":\\\"5000\\\",\\\"enableLogging\\\":true,\\\"loggingEndpoint\\\":\\\"https:\\\/\\\/adexp.liftoff.io\\\"},\\\"clickConfig\\\":{\\\"clickthroughURL\\\":{\\\"url\\\":\\\"https:\\\/\\\/play.google.com\\\/store\\\/apps\\\/details%3Fid=com.playrix.township\\\",\\\"type\\\":2},\\\"clickTrackingURLs\\\":%5B{\\\"url\\\":\\\"https:\\\/\\\/click.liftoff.io\\\/v1\\\/campaign_click\\\/Mg7kXlNeI6IpbPMmKzZY_ztMYM6NO1OeUtL7NsADF-hcIl_fVATEOtZ5jelfNO7I3TKARpSfHHHxEXfDLJalv9ui50FzdKTT3J15quufe6oxCz-RHA4LAZH70RhIJ6E29NjJFl0lG_8JKgaH29DOceobtRV7Um0DSfKEnyyGHg_P87C3QOyQLZD4oIlLSpdfr0BBoUvH_3yIq9WNf6VG6eltwUSDd_ONKwaeEjbX0pCLDTr9R-HIfxpmb4LyTx0otoP6tRnS-QrE0tYnlFpMyjcHaArwt2f6_48fwWEdREjOVek8RDeptq7HNiOnRVLbbCdWXb9F1isw9jjphxlFEZZOhGU10iRpylSmKZw7WmPt2EVhcdsy_KWhe-KkNXWm-O8PUzqZNxKoM9-z5wgbZmJrOdgq0IHbbY-iQQVr640w3mPnnoGqGZBAj8PS2CLGNDCd8oCFe0PuQpsykAJ4ZeUwrq3S7TOvKqpd5_Bcpb1_pXitJ7UBh7l4yeb5gl9udGXyE02dysrtz2BICk4Rvopw2FwPPXWlEWsOF-lkx2QYQ9Pu2Y5MYa62ow0qqhcaogU6uj0ghqKqjG_mfw%3Fvast_el=3\\\",\\\"type\\\":1}%5D},\\\"cdnURL\\\":\\\"https:\\\/\\\/cdn.liftoff.io\\\",\\\"geo\\\":{\\\"latitude\\\":-7.2484,\\\"longitude\\\":112.7419},\\\"creative\\\":{\\\"id\\\":213371,\\\"width\\\":480,\\\"height\\\":320,\\\"name\\\":\\\"%28image211%29480x320_ts_video661v1_nst_en_30s_20mb_options_playable124\\\",\\\"params\\\":%5B%5D},\\\"abTests\\\":%5B\\\"click-waterfall-v2-control\\\",\\\"vast-html-endscreen-control\\\",\\\"ios-html-meta-header-control\\\",\\\"csp-srcdoc-priority-control\\\",\\\"app-store-modal-control\\\"%5D,\\\"app\\\":{\\\"id\\\":\\\"com.os.falcon.bob2.adventure.world\\\",\\\"name\\\":\\\"Bob%27s World 2 - Running game\\\"},\\\"campaign\\\":{\\\"id\\\":15373,\\\"name\\\":\\\"TS_GP_AP_Low\\\",\\\"params\\\":%5B%5D},\\\"creativePolicy\\\":{\\\"animationDurationLimit\\\":0,\\\"audioPolicy\\\":\\\"always-mute\\\",\\\"russianAgeRating\\\":null,\\\"removeAdWrapper\\\":false,\\\"showAdChoices\\\":false,\\\"addBorder\\\":false,\\\"useCustomClose\\\":false,\\\"closeDelay\\\":5,\\\"blockNotifications\\\":false,\\\"showChineseWatermark\\\":false,\\\"blockStrobing\\\":false},\\\"device\\\":{\\\"googleAID\\\":\\\"aa9f2aa4-845d-4bfe-bc6b-9150e1b1551d\\\",\\\"connectionType\\\":3,\\\"googleAIDSHA1\\\":\\\"b34af918dd77461b498a5af0e54d84895de14ed8\\\",\\\"ip\\\":\\\"112.215.237.195\\\",\\\"idfaSHA1\\\":null,\\\"androidIDMD5\\\":null,\\\"idfa\\\":null,\\\"normalizedLanguage\\\":\\\"id\\\",\\\"osVersion\\\":\\\"11\\\",\\\"idfaMD5\\\":null,\\\"androidIDSHA1\\\":null,\\\"androidID\\\":null,\\\"platform\\\":\\\"android\\\",\\\"model\\\":\\\"\\\"},\\\"trackingToken\\\":\\\"v.2_g.125661_a.61516e15294ecded58f89c8e_c.24_t.ua_u.b34af918dd77461b\\\",\\\"exchange\\\":\\\"vungle\\\",\\\"isStaffDevice\\\":false,\\\"platform\\\":\\\"android\\\"}\')),scriptSrcURLs: [\\\"https:\\\/\\\/cdn.liftoff.io\\\/resources\\\/polyfills-33c384a010d661c2a64d.js\\\",\\\"https:\\\/\\\/cdn.liftoff.io\\\/resources\\\/inner_env-bfa56fb84006156f82f7.js\\\"],rootURL: \\\"https:\\\/\\\/cdn.liftoff.io\\\/customers\\\/753\\\/creatives\\\/205394\\\/\\\",html: \'%3C%21DOCTYPE html%3E%3Chtml%3E%3Chead%3E%3Cmeta charset=\\\"utf-8\\\"%3E%3Ctitle%3EPlayable%3C\\\/title%3E%3Cmeta name=\\\"viewport\\\" content=\\\"width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover\\\"%3E%3C\\\/head%3E%3Cbody%3E%3Cscript type=\\\"text\\\/javascript\\\"%3Ewindow.apiName=\\\"liftoff\\\"%3Bwindow.playableEnv={\\\"lang\\\":\\\"en\\\",\\\"apiName\\\":\\\"liftoff\\\",\\\"nameGameAbbr\\\":\\\"ts\\\",\\\"params\\\":{\\\"showInstallButton\\\":true}}%3C\\\/script%3E%3Cdiv id=\\\"styles-container\\\"%3E%3C\\\/div%3E%3Cdiv id=\\\"scripts-container\\\"%3E%3C\\\/div%3E%3Cscript type=\\\"text\\\/javascript\\\"%3Ewindow.addEventListener%28\\\"load\\\",function%28%29{var is_ready_app,is_ready_timer,ROOT_URL=\\\"\\\"%3B\\\"undefined\\\"%21=typeof LIFTOFF_ROOT_URL%26%26%28ROOT_URL=LIFTOFF_ROOT_URL%29%3Bvar name,cb,style,counter=0%3Bfunction next%28%29{loader.create%28%29,setTimeout%28function%28%29{is_ready_timer=%210,init%28%29},1e3%29,js%28\\\"app.js\\\",function%28%29{is_ready_app=%210,init%28%29}%29}function init%28%29{is_ready_timer%26%26is_ready_app%26%26%28\\\"undefined\\\"%21=typeof superApp%3FsuperApp.init%28%29:initGame%28%29,\\\"undefined\\\"%21=typeof loader%26%26loader.clear%28%29%29}function js%28name,cb%29{var script=document.createElement%28\\\"script\\\"%29%3Bscript.src=ROOT_URL+name,document.getElementById%28\\\"scripts-container\\\"%29.appendChild%28script%29,script.onload=function%28%29{cb%26%26cb%28%29}}js%28\\\"loader.js\\\",function%28%29{2==++counter%26%26next%28%29}%29,name=\\\"styles.css\\\",cb=function%28%29{2==++counter%26%26next%28%29},%28style=document.createElement%28\\\"link\\\"%29%29.href=ROOT_URL+name,style.type=\\\"text\\\/css\\\",style.rel=\\\"stylesheet\\\",style.media=\\\"screen,print\\\",document.getElementById%28\\\"styles-container\\\"%29.appendChild%28style%29,style.onload=function%28%29{cb%26%26cb%28%29},window.clickInstall=function%28%29{window.open%28window._LIFTOFF_ENV.pinpointURL,\\\"_blank\\\"%29}}%29%3B%3C\\\/script%3E%3C\\\/body%3E%3C\\\/html%3E\',externalHtmlURL: null,});<\\\/script><\\\/div>]]><\\\/HTMLResource><TrackingEvents><Tracking event=\\\"creativeView\\\"><![CDATA[https:\\\/\\\/adexp.liftoff.io\\\/event\\\/vast\\\/htmlEndscreenView\\\/c9dfb5CN3VBxIYNjE1MTZlMTUyOTRlY2RlZDU4Zjg5YzhlGIiE2LDCLyAYKPuCDTCbCzoiY29tLm9zLmZhbGNvbi5ib2IyLmFkdmVudHVyZS53b3JsZEIaY2xpY2std2F0ZXJmYWxsLXYyLWNvbnRyb2xCG3Zhc3QtaHRtbC1lbmRzY3JlZW4tY29udHJvbEIcaW9zLWh0bWwtbWV0YS1oZWFkZXItY29udHJvbEIbY3NwLXNyY2RvYy1wcmlvcml0eS1jb250cm9sQhdhcHAtc3RvcmUtbW9kYWwtY29udHJvbEoKNDFjMjE4YjEzNFADWgNJRE5gAmgEcg5hcC1ub3J0aGVhc3QtMYABGJIBAmlkmAECoQEzMzMzMzOzP6oBCDE2NDB4ODEwsgEJQWR2ZW50dXJlugEcQm9iJ3MgV29ybGQgMiAtIFJ1bm5pbmcgZ2FtZcIBGXZhc3QtY2RiNDU5ZDNjNjViMTdkODdlMGLKAQIBAtIBAA?playhead=[CONTENTPLAYHEAD]&sr=1]]><\\\/Tracking><\\\/TrackingEvents><\\\/Companion><\\\/CompanionAds><\\\/Creative><\\\/Creatives><Description><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\\/Description><Survey><\\\/Survey><Extensions><Extension type=\\\"AdVerifications\\\"><AdVerifications><Verification vendor=\\\"moat.com-omsdkvungleinappvideo781943494431\\\"><JavaScriptResource apiFramework=\\\"omid\\\" browserOptional=\\\"true\\\"><![CDATA[https:\\\/\\\/z.moatads.com\\\/omsdkvungleinappvideo781943494431\\\/moatvideo.js]]><\\\/JavaScriptResource><VerificationParameters><![CDATA[{\\\"moatClientLevel1\\\":\\\"{{{app_id}}}\\\",\\\"moatClientLevel2\\\":\\\"{{{campaign_id}}}\\\",\\\"moatClientLevel3\\\":\\\"{{{creative_id}}}\\\",\\\"moatClientLevel4\\\":\\\"{{{placement_id}}}\\\",\\\"moatClientSlicer1\\\":\\\"{{{pub_app_id}}}\\\",\\\"moatClientLevel5\\\":\\\"{{{rtb_deal_id}}}\\\",\\\"moatClientLevel6\\\":\\\"{{{rtb_connection_id}}}\\\"}]]><\\\/VerificationParameters><\\\/Verification><\\\/AdVerifications><\\\/Extension><Extension type=\\\"Extra\\\"><CTA><![CDATA[\\u70B9\\u51FB\\u4E0B\\u8F7D]]><\\\/CTA><SystemIcon><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/07c04164de3140d2cfe4bdd9812aef22~c1_0x0_q100.png]]><\\\/SystemIcon><FullStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/48c275deda9f2daa92acccf8218fc59f~c1_0x0_q100.jpeg]]><\\\/FullStar><HalfStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/b273598ab25fec09a467d2b895e3c53e~c1_0x0_q100.jpeg]]><\\\/HalfStar><EmptyStar><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/fedbae142b79804e383eed3f4d06e9d5~c1_0x0_q100.jpeg]]><\\\/EmptyStar><Review><![CDATA[https:\\\/\\\/sf1-ttcdn-tos.pstatp.com\\\/img\\\/ad.union.api\\\/297845a2690ec96bd1290a0a289ab373~c1_0x0_q100.jpeg]]><\\\/Review><MoPubCtaText><\\\/MoPubCtaText><\\\/Extension><Extension type=\\\"Vungle\\\"><ASODOption><VungleEndCard><enable>true<\\/enable><\\/VungleEndCard><AppStoreOnVideo><OnClose>true<\\\/OnClose><OnDelayMs>2000<\\\/OnDelayMs><\\\/AppStoreOnVideo><AppStoreOnVideoEndCard><OnClose>true<\\\/OnClose><OnDelayMs>3000<\\\/OnDelayMs><\\\/AppStoreOnVideoEndCard><\\\/ASODOption><\\\/Extension><\\\/Extensions><\\\/InLine><\\\/Ad><\\\/VAST>"'
        over_ride_adm = over_ride_adm.replace("\\\\", "\\")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger',
                                          override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "VX_ENDCARD")
        assert_that(normal_replacements["VX_ENDCARD"], equal_to('true'))
        assert_that(normal_replacements["STATIC_EC_CLOSE_BUTTON_DELAY_SECONDS"], equal_to('6'))

    @allure.feature('close button padding')
    @allure.tag('basic')
    @allure.story('VM-81 make the size of close button padding area configurable--exchange server work')
    @allure.description('Verify that close button is configable')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_close_button_01(self, pub_app_id, placement, sdk_v, rtb_ids):
        """
        pub account config:
        close_button_padding:10
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "CLOSE_BUTTON_PADDING")
        assert_that(normal_replacements["CLOSE_BUTTON_PADDING"], equal_to('10px'))

    @allure.feature('close button padding')
    @allure.tag('basic')
    @allure.story('VM-81 make the size of close button padding area configurable--exchange server work')
    @allure.description('Verify that close button is configable')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    @pytest.mark.parametrize('placement', [android_common_coppa_placememt])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_close_button_02(self, pub_app_id, placement, sdk_v, rtb_ids):
        """

        pub account config:
        close_button_padding:0
        """
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "CLOSE_BUTTON_PADDING")
        assert_that(normal_replacements["CLOSE_BUTTON_PADDING"], equal_to('0px'))

    @allure.feature('close button padding')
    @allure.tag('basic')
    @allure.story('VM-81 make the size of close button padding area configurable--exchange server work')
    @allure.description('Verify that close button default value')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_close_button_03(self, pub_app_id, placement, sdk_v, rtb_ids):
        """

        pub account config:
        no close_button_padding field
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "CLOSE_BUTTON_PADDING")
        assert_that(normal_replacements["CLOSE_BUTTON_PADDING"], equal_to('0px'))

    @allure.feature('incentivized token')
    @allure.tag('basic', 'v1.260.0')
    @allure.story('VM-139 Add INCENTIVIZED token to ads response')
    @allure.description('Verify that incentivized token is added for rewarded placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_incentivized_token_01(self, pub_app_id, placement, sdk_v, rtb_ids):
        """
        placement:
        type:rewarded
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'INCENTIVIZED')
        assert_that(normal_replacements['INCENTIVIZED'], equal_to("true"))

    @allure.feature('incentivized token')
    @allure.tag('basic', 'v1.260.0')
    @allure.story('VM-139 Add INCENTIVIZED token to ads response')
    @allure.description('Verify that incentivized token is added for rewarded placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_incentivized_token_02(self, pub_app_id, placement, sdk_v, rtb_ids):
        """
        pub app:
        type:interstitial
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'INCENTIVIZED')
        assert_that(normal_replacements['INCENTIVIZED'], equal_to("false"))

    @allure.feature('session id')
    @allure.tag('basic', 'v1.260.0')
    @allure.story('VM-146 Request to add the SESSION ID for programmatic ads.')
    @allure.description('Verify the SESSION ID token is added')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_session_id_01(self, pub_app_id, placement, sdk_v, rtb_ids):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        event_id = ad_markup['id']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "SESSION_ID")
        assert_that(normal_replacements["SESSION_ID"], equal_to(event_id))

    @allure.feature('session id')
    @allure.tag('basic', 'v1.260.0')
    @allure.story('VM-146 Request to add the SESSION ID for programmatic ads.')
    @allure.description('Verify the SESSION ID token should not be added for native placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_session_id_02(self, pub_app_id, placement, sdk_v, rtb_ids):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        event_id = ad_markup['id']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_not_exist(normal_replacements, "SESSION_ID")