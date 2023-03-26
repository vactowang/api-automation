import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_hb_win_notification, request_ads_ios
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema




@allure.epic('scrat - report ad - v5')
class TestReportAdMessage(object):

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke', 'v0.162.0')
    @allure.story('report ad message from debug info'
                  'PBJ-4757 Support Network Fraud Request blocking by device IDs')
    @allure.description('Verify report ad message from debug info'
                        'Verify that the same event id will be blocked')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('hb', [True, False])
    def test_report_ad_message_basic(self, pub_app_id, hb):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=hb,
                                               app_id=test_app_id_ios)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        if 'msg' in debug:
            assert_that(debug['msg'],equal_to('event_duplicated'))
        else:
            assert_keys_exist(debug, 'report_ad_message')
            assert_that(debug['report_ad_message']['vungleType'], equal_to('reportAd'))
            assert_that(isinstance(debug['report_ad_message']['timestamp'], str))
            assert_that(isinstance(debug['report_ad_message']['is_demand_third_party'], bool))
            assert_that(isinstance(debug['report_ad_message']['scrat_version'], str))
            assert_that(isinstance(debug['report_ad_message']['scrat_cloud_provider'], str))


    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad message from debug info')
    @allure.description('Verify report ad message plays from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_plays(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(isinstance(debug['report_ad_message']['plays'][0]['startTime'], int))
        assert_that(isinstance(debug['report_ad_message']['plays'][0]['videoViewed'], int))
        assert_that(isinstance(debug['report_ad_message']['plays'][0]['videoLength'], int))

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad message from debug info')
    @allure.description('Verify report ad message clickedThrough from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_clicked_through(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(set(debug['report_ad_message']['clickedThrough']).issubset(
            ['download', 'mraidOpen', 'mraidClose']))

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad message from debug info')
    @allure.description('Verify report ad message locale from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_locale(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=gb_ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['country'], equal_to('GB'))
        assert_that(isinstance(debug['report_ad_message']['region'], str))
        assert_that(isinstance(debug['report_ad_message']['city'], str))
        assert_that(isinstance(debug['report_ad_message']['iso2_language'], str))
        assert_that(isinstance(debug['report_ad_message']['timezone'], str))

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad message from debug info')
    @allure.description('Verify report ad message device info from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_device_info(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, os_version='13',
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=gb_ip,
                                                                                    sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(isinstance(debug['report_ad_message']['device_language'], str))
        assert_that(debug['report_ad_message']['device_user_agent'], equal_to(req['device']['ua']))
        assert_that(debug['report_ad_message']['device_make'], equal_to('iPhone12'))
        assert_that(debug['report_ad_message']['device_model'], equal_to('5'))
        assert_that(isinstance(debug['report_ad_message']['device_height'], int))
        assert_that(isinstance(debug['report_ad_message']['device_width'], int))
        assert_that(debug['report_ad_message']['os_version'], equal_to('13'))
        assert_that(debug['report_ad_message']['platform'], equal_to('iOS'))
        assert_that(isinstance(debug['report_ad_message']['volume'], float))
        assert_that(isinstance(debug['report_ad_message']['battery_optimization'], bool))
        assert_that(debug['report_ad_message']['ip_address'], equal_to(gb_ip))
        assert_that(isinstance(debug['report_ad_message']['connection'], str))
        assert_that(isinstance(debug['report_ad_message']['network_operator'], str))
        assert_that(debug['report_ad_message']['user_agent'], equal_to('Vungle/6.8.0'))
        assert_that(debug['report_ad_message']['device_id'], equal_to(test_ifa))
        assert_that(debug['report_ad_message']['device_id_source'], equal_to('IFA'))
        assert_that(debug['report_ad_message']['ifa'], equal_to(test_ifa))
        assert_that(debug['report_ad_message']['isu'], equal_to(test_ifa))

    @allure.feature('user privacy')
    @allure.tag('gdpr')
    @allure.story('report ad message gdpr info from debug info')
    @allure.description('Verify report ad message gdpr info from debug info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_report_ad_message_device_id_not_null(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, gdpr=consent_status,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                assert_that(debug['report_ad_message']['device_id'], not equal_to(test_ifa))
                assert_that(debug['report_ad_message']['device_id_source'], equal_to('GDPR'))
                assert_keys_not_exist(debug['report_ad_message'], 'ifa')
                assert_keys_not_exist(debug['report_ad_message'], 'isu')
            else:
                assert_that(debug['report_ad_message']['device_id'], equal_to(test_ifa))
                assert_that(debug['report_ad_message']['device_id_source'], equal_to('IFA'))
                assert_that(debug['report_ad_message']['ifa'], equal_to(test_ifa))
                assert_that(debug['report_ad_message']['isu'], equal_to(test_ifa))
        else:
            if ip == eu_country_ip and consent_status == 'opted_out':
                assert_that(debug['report_ad_message']['device_id'], not equal_to(test_ifa))
                assert_that(debug['report_ad_message']['device_id_source'], equal_to('GDPR'))
                assert_keys_not_exist(debug['report_ad_message'], 'ifa')
                assert_keys_not_exist(debug['report_ad_message'], 'isu')
            else:
                assert_that(debug['report_ad_message']['device_id'], equal_to(test_ifa))
                assert_that(debug['report_ad_message']['device_id_source'], equal_to('IFA'))
                assert_that(debug['report_ad_message']['ifa'], equal_to(test_ifa))
                assert_that(debug['report_ad_message']['isu'], equal_to(test_ifa))

    @allure.feature('user privacy')
    @allure.tag('gdpr')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify the device id info in report ad message from debug info when device id is null')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_report_ad_message_device_id_null(self, pub_app_id, consent_status, ip):
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa='', gdpr=consent_status, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                assert_that(debug['report_ad_message']['device_id'], not equal_to(''))
                assert_that(debug['report_ad_message']['device_id_source'], equal_to('Vungle_FP'))
                assert_keys_not_exist(debug['report_ad_message'], 'ifa')
                assert_keys_not_exist(debug['report_ad_message'], 'isu')
            else:
                assert_that(debug['report_ad_message']['device_id'], not equal_to(''))
                assert_that(debug['report_ad_message']['device_id_source'], equal_to('Vungle_FP'))
                assert_keys_not_exist(debug['report_ad_message'], 'ifa')
                assert_that(debug['report_ad_message']['isu'], not equal_to(''))
        else:
            if ip == eu_country_ip and consent_status == 'opted_out':
                assert_that(debug['report_ad_message']['device_id'], not equal_to(''))
                assert_that(debug['report_ad_message']['device_id_source'], equal_to('Vungle_FP'))
                assert_keys_not_exist(debug['report_ad_message'], 'ifa')
                assert_keys_not_exist(debug['report_ad_message'], 'isu')
            else:
                assert_that(debug['report_ad_message']['device_id'], not equal_to(''))
                assert_that(debug['report_ad_message']['device_id_source'], equal_to('Vungle_FP'))
                assert_keys_not_exist(debug['report_ad_message'], 'ifa')
                assert_that(debug['report_ad_message']['isu'], not equal_to(''))

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad message from debug info')
    @allure.description('Verify report ad message pub info from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_pub_info(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['pub_app_id'], equal_to(common_test_app))
        assert_that(debug['report_ad_message']['pub_app_bundle_id'], equal_to(req['app']['bundle']))
        assert_that(isinstance(debug['report_ad_message']['pub_app_market_id'], str))
        assert_that(debug['report_ad_message']['placement_reference_id'], equal_to(common_test_placement))

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad message from debug info')
    @allure.description('Verify report ad message app info from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_app_info(self, pub_app_id):
        test_ifa = gen_device_id()
        app_id = gen_test_app_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=app_id)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['ad_app_id'],
                    equal_to(app_id.replace('\"', '"').split('"')[3]))
        assert_that(debug['report_ad_message']['ad_app_object_id'],
                    equal_to(app_id.replace('\"', '"').split('"')[3]))
        assert_that(debug['report_ad_message']['event_id'],
                    equal_to(app_id.replace('\"', '"').split('"')[-2]))

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad message from debug info')
    @allure.description('Verify report ad message campaign info from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_campaign_info(self, pub_app_id):
        test_ifa = gen_device_id()
        app_id = gen_test_app_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=app_id)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['campaign_id'], equal_to(test_campaign_ios.split('|')[0]))
        assert_that(debug['report_ad_message']['creative_id'], equal_to(test_campaign_ios.split('|')[1]))
        assert_that(debug['report_ad_message']['strategy'], equal_to(test_campaign_ios.split('|')[2]))
        assert_that(debug['report_ad_message']['event_id'], equal_to(app_id.replace('\"', '"').split('"')[-2]))
        assert_that(isinstance(debug['report_ad_message']['campaign_rate'], int))
        assert_that(isinstance(debug['report_ad_message']['campaign_rate_type'], str))

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP to SDK')
    @allure.description('Verify report ad message campaign info from debug info for real edsp crid')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_report_ad_message_campaign_info_edsp(self, pub_app_id, header_bidding):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa,
                                               campaign=test_campaign_default_edsp, header_bidding=header_bidding, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat',
                                                                                    sdk_version='Vungle/6.10.6',
                                                                                    ))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['campaign_id'], equal_to(test_campaign_default_edsp.split('|')[0].split('_')[1]))
        assert_that(debug['report_ad_message']['creative_id'], equal_to(test_campaign_default_edsp.split('|')[1].split('_')[1]))
        assert_that(debug['view_message']['campaign_id'],
                    equal_to(test_campaign_default_edsp.split('|')[0].split('_')[1]))
        assert_that(debug['view_message']['creative_id'],
                    equal_to(test_campaign_default_edsp.split('|')[1].split('_')[1]))


    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP to SDK')
    @allure.description('Verify report ad message campaign info from debug info for crid& cid not existing in DB')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_report_ad_message_campaign_info_edsp_not_in_db(self, pub_app_id, header_bidding):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa,
                                               campaign=test_campaign_edsp_not_in_db, header_bidding=header_bidding, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat',
                                                                                    sdk_version='Vungle/6.10.6',
                                                                                    ))
        logging.info(r.status_code)
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['campaign_id'], equal_to(test_campaign_edsp_not_in_db.split('|')[0].split('_')[1]))
        assert_that(debug['report_ad_message']['creative_id'], equal_to(test_campaign_edsp_not_in_db.split('|')[1].split('_')[1]))
        assert_that(debug['view_message']['campaign_id'],
                    equal_to(test_campaign_edsp_not_in_db.split('|')[0].split('_')[1]))
        assert_that(debug['view_message']['creative_id'],
                    equal_to(test_campaign_edsp_not_in_db.split('|')[1].split('_')[1]))




    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad message from debug info')
    @allure.description('Verify report ad message ad info from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_ad_info(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['ad_start_time'], equal_to(req['request']['adStartTime']))
        assert_that(debug['report_ad_message']['ad_duration'], equal_to(req['request']['adDuration']))
        if 'download' in req['request']['clickedThrough']:
            assert_that(debug['report_ad_message']['ad_clicked'], equal_to(True))
        else:
            assert_that(debug['report_ad_message']['ad_clicked'], equal_to(False))
        assert_that(debug['report_ad_message']['ad_size'], equal_to(req['request']['ad_size']))
        assert_that(debug['report_ad_message']['ad_type'], is_in(['video', 'banner']))
        assert_that(isinstance(debug['report_ad_message']['completed_view'], bool))
        assert_that(isinstance(debug['report_ad_message']['view'], bool))
        assert_that(debug['report_ad_message']['ordinal_view'], equal_to(req['request']['ordinal_view']))
        assert_that(debug['report_ad_message']['time_to_download'], equal_to(req['request']['ttDownload']))
        assert_that(debug['report_ad_message']['init_time'], equal_to(req['request']['init_timestamp']))
        assert_that(debug['report_ad_message']['download_start_time'],
                    equal_to(req['request']['asset_download_duration']))


    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3937 Server side be able to process StoreKit overlay auto show event in the ReportAd '
                  '(SKO Phase 2.5)')
    @allure.description('Verify the value of sko_auto_show in the message if w/, W/o \'skoAutoShow\' '
                        'in request clickthrough and will not impact download action' )
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('skoAutoshow', [True, False])
    def test_report_ad_message_skoAutoShow_info(self, pub_app_id, skoAutoshow):
        test_ifa = gen_device_id()

        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, skoAutoshow=skoAutoshow,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['ad_start_time'], equal_to(req['request']['adStartTime']))
        assert_that(debug['report_ad_message']['ad_duration'], equal_to(req['request']['adDuration']))
        if 'download' in req['request']['clickedThrough']:
            assert_that(debug['report_ad_message']['ad_clicked'], equal_to(True))
        else:
            assert_that(debug['report_ad_message']['ad_clicked'], equal_to(False))
        if 'skoAutoShow' in req['request']['clickedThrough']:
            assert_that(debug['report_ad_message']['sko_auto_show'], equal_to(True))
        else:
            assert_that(debug['report_ad_message']['sko_auto_show'], equal_to(False))



    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad message from debug info')
    @allure.description('Verify report ad message imp info from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_imp_info(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['incentivized'], equal_to(req['request']['incentivized']))
        assert_that(isinstance(debug['report_ad_message']['video_id'], str))
        assert_that(isinstance(debug['report_ad_message']['video_object_id'], str))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'R_0.101.0')
    @allure.story('PBJ-1954 SKAdNetwork support - Add pub_app_market_id to reportad')
    @allure.description('Verify report ad message pub info from debug info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_pub_app_market_id(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['pub_app_market_id'], equal_to('1131184101'))

    @allure.feature('test mode flag')
    @allure.tag('normal', 'test_mode', 'R_0.104.0')
    @allure.story('PBJ-2031 Scrat test mode flag')
    @allure.description('Verify report ad message test mode flag from debug info in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_test_mode_flag_1(self, pub_app_id):
        test_ifa = gen_device_id()
        ads_response = request_ads_ios(pub_app_id, common_test_placement, test_ifa=test_ifa)
        campaign = ads_response['ads'][0]['ad_markup']['campaign']
        campaign = "61cdbb3eeb0c050016d79833|61cdbca7eb0c050016d79836|datasci--blr_ado_ios_wf--{\"skan-model\":null}--success--meister|63ae627147398157d3402ede"
        test_mode_campaign = campaign.split('|')[0] + '|' + campaign.split('|')[1] + '|test-ads|' \
                             + campaign.split('|')[3]
        app_id = ads_response['ads'][0]['ad_markup']['app_id']
        ad_token = ads_response['ads'][0]['ad_markup']['ad_token']
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=True,
                                               app_id=app_id, campaign=test_mode_campaign, ad_token=ad_token)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['is_test'], equal_to(True))

    @allure.feature('test mode flag')
    @allure.tag('normal', 'R_0.104.0')
    @allure.story('PBJ-2031 Scrat test mode flag')
    @allure.description('Verify report ad message test mode flag from debug info in non test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_test_mode_flag_2(self, pub_app_id):
        test_ifa = gen_device_id()
        ads_response = request_ads_ios(pub_app_id, common_test_placement, test_ifa=test_ifa)
        campaign = ads_response['ads'][0]['ad_markup']['campaign']
        app_id = ads_response['ads'][0]['ad_markup']['app_id']
        ad_token = ads_response['ads'][0]['ad_markup']['ad_token']
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=True,
                                               app_id=app_id, campaign=campaign, ad_token=ad_token)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug['report_ad_message'], 'is_test')

    # @allure.feature('banner support')
    # @allure.tag('normal', 'R_0.109.0')
    # @allure.story('PBJ-2217 Discrepancy issue for invisible banners')
    # @allure.description('Verify the completed view value in report ad message for banner is always true')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_banner_placement])
    # @pytest.mark.parametrize('complete', [True, False])
    # def test_report_ad_message_banner_1(self, pub_app_id, placement, complete):
    #     test_ifa = gen_device_id()
    #     ads_response = request_ads_ios(pub_app_id, placement, test_ifa=test_ifa, banner=True, hb=False, ip=gb_ip
    #                                    )
    #     if 'sleep' not in ads_response['ads'][0]['ad_markup']:
    #         campaign = ads_response['ads'][0]['ad_markup']['campaign']
    #         app_id = ads_response['ads'][0]['ad_markup']['app_id']
    #         ad_token = ads_response['ads'][0]['ad_markup']['ad_token']
    #         req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, app_id=app_id, campaign=campaign,
    #                                                ad_token=ad_token, viewed=True, completed_viewed=complete)
    #         r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
    #
    #         response_payload = r.json()
    #         debug = response_payload['ext']['debug']
    #         assert_response_status_code(r.status_code, HTTPStatus.OK)
    #         assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
    #         assert_that(debug['report_ad_message']['completed_view'], equal_to(True))

    # @allure.feature('banner support')
    # @allure.tag('normal', 'R_0.109.0')
    # @allure.story('PBJ-2217 Discrepancy issue for invisible banners')
    # @allure.description('Verify the viewed value in report ad message for internal banner which videoViewed > 0')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_banner_placement])
    # def test_report_ad_message_discrepancy_issue_1(self, pub_app_id, placement):
    #     test_ifa = gen_device_id()
    #     ads_response = request_ads_ios(pub_app_id, placement, test_ifa=test_ifa, banner=True, hb=False, ip=gb_ip)
    #     if 'sleep' not in ads_response['ads'][0]['ad_markup']:
    #         campaign = ads_response['ads'][0]['ad_markup']['campaign']
    #         app_id = ads_response['ads'][0]['ad_markup']['app_id']
    #         ad_token = ads_response['ads'][0]['ad_markup']['ad_token']
    #         req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, app_id=app_id, campaign=campaign,
    #                                                ad_token=ad_token)
    #         r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
    #
    #         response_payload = r.json()
    #         debug = response_payload['ext']['debug']
    #         assert_response_status_code(r.status_code, HTTPStatus.OK)
    #         assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
    #         assert_that(debug['report_ad_message']['view'], equal_to(True))

    # @allure.feature('banner support')
    # @allure.tag('normal', 'R_0.109.0')
    # @allure.story('PBJ-2217 Discrepancy issue for invisible banners')
    # @allure.description('Verify the viewed value in report ad message for internal banner which videoViewed = 0')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_banner_placement])
    # def test_report_ad_message_discrepancy_issue_2(self, pub_app_id, placement):
    #     test_ifa = gen_device_id()
    #     ads_response = request_ads_ios(pub_app_id, placement, test_ifa=test_ifa, banner=True, hb=False, ip=gb_ip)
    #     if 'sleep' not in ads_response['ads'][0]['ad_markup']:
    #         campaign = ads_response['ads'][0]['ad_markup']['campaign']
    #         app_id = ads_response['ads'][0]['ad_markup']['app_id']
    #         ad_token = ads_response['ads'][0]['ad_markup']['ad_token']
    #         req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, app_id=app_id, campaign=campaign,
    #                                                ad_token=ad_token, viewed=False)
    #         r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
    #
    #         response_payload = r.json()
    #         debug = response_payload['ext']['debug']
    #         assert_response_status_code(r.status_code, HTTPStatus.OK)
    #         assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
    #         assert_that(debug['report_ad_message']['view'], equal_to(False))

    @allure.feature('ad format')
    @allure.tag('normal', 'v0.114.0', 'ad_format')
    @allure.story('PBJ-2588 New field in as_reportAds topic')
    @allure.description('Verify the download field from report ad message')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_report_ad_message_download_1(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        ads_response = request_ads_ios(pub_app_id, placement, test_ifa=test_ifa)
        if 'sleep' not in ads_response['ads'][0]['ad_markup']:
            campaign = ads_response['ads'][0]['ad_markup']['campaign']
            app_id = ads_response['ads'][0]['ad_markup']['app_id']
            ad_token = ads_response['ads'][0]['ad_markup']['ad_token']
            req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, app_id=app_id,
                                                   campaign=campaign, ad_token=ad_token, download=1)
            r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

            response_payload = r.json()
            debug = response_payload['ext']['debug']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
            assert_that(debug['report_ad_message']['download'], equal_to(1))

    @allure.feature('ad format')
    @allure.tag('normal', 'v0.114.0', 'ad_format')
    @allure.story('PBJ-2588 New field in as_reportAds topic')
    @allure.description('Verify there is no download field from report ad message if no download from plays')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('download', [None, 'abcdef'])
    def test_report_ad_message_download_2(self, pub_app_id, placement, download):
        test_ifa = gen_device_id()
        ads_response = request_ads_ios(pub_app_id, placement, test_ifa=test_ifa)
        if 'sleep' not in ads_response['ads'][0]['ad_markup']:
            campaign = ads_response['ads'][0]['ad_markup']['campaign']
            app_id = ads_response['ads'][0]['ad_markup']['app_id']
            ad_token = ads_response['ads'][0]['ad_markup']['ad_token']
            req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, app_id=app_id,
                                                   campaign=campaign, ad_token=ad_token, download=download)
            r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

            response_payload = r.json()
            debug = response_payload['ext']['debug']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
            assert_keys_not_exist(debug['report_ad_message'], 'download')

    @allure.feature('idfv message')
    @allure.tag('normal', 'v0.115.0')
    @allure.story('PBJ-2635 IDFV field in as-views topic')
    @allure.description('Verify the idfv field from as report ad')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_report_ad_message_idfv_1(self, pub_app_id, placement, device_id):
        test_ifa = device_id
        test_idfv = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, idfv=test_idfv, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['device_id_source'], equal_to('IDFV'))
        assert_that(debug['report_ad_message']['idfv'], equal_to(test_idfv))

    @allure.feature('idfv message')
    @allure.tag('normal', 'v0.115.0')
    @allure.story('PBJ-2635 IDFV field in as-views topic')
    @allure.description('Verify the idfv field from as report ad')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_report_ad_message_idfv_2(self, pub_app_id, placement, device_id):
        test_ifa = device_id
        test_idfv = ''

        req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, idfv=test_idfv, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['device_id_source'], equal_to('Vungle_FP'))
        assert_keys_not_exist(debug['report_ad_message'], 'idfv')

    @allure.feature('deeplink message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3254  Deeplink report/metric in scrat')
    @allure.description('Verify there is deeplinkSuccess info logged in message')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('hb', [True, False])
    def test_deeplink_success_logged(self, pub_app_id, hb):
        test_app_id = gen_test_app_id()
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=hb,
                                               app_id=test_app_id)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat',
                                                                                    rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['deep_link_success'], equal_to(True))

    @allure.feature('deeplink message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3254  Deeplink report/metric in scrat')
    @allure.description('Verify there is no deeplinkSuccess info logged in message')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_deeplink_success_not_logged_01(self, pub_app_id):
        test_ifa = gen_device_id()
        test_app_id = gen_test_app_id()
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa,
                                               deeplink='deeplinksuccess', app_id=test_app_id)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat',
                                                                                    rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug['report_ad_message'], 'deep_link_success')

    @allure.feature('deeplink message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3254  Deeplink report/metric in scrat')
    @allure.description('Verify there is no deeplinkSuccess info logged in message')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_deeplink_success_not_logged_02(self, pub_app_id):
        test_ifa = gen_device_id()
        test_app_id = gen_test_app_id()
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa,
                                               deeplink='deeplink Success', app_id=test_app_id)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat',
                                                                                    rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug['report_ad_message'], 'deep_link_success')

    @allure.feature('deeplink message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3254  Deeplink report/metric in scrat')
    @allure.description('Verify there is deeplinkSuccess info logged in message on android')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('hb', [True, False])
    def test_deeplink_success_logged_android(self, pub_app_id, hb):
        test_app_id = gen_test_app_id('android')
        req = request_payload.report_ad_v5_android(pub_app_id, common_test_placement, header_bidding=hb, app_id=test_app_id)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat',
                                                                                    rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['deep_link_success'], equal_to(True))

    @allure.feature('deeplink message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3254  Deeplink report/metric in scrat')
    @allure.description('Verify there is no deeplinkSuccess info logged in message on android')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('hb', [True, False])
    def test_no_deeplink_success_logged_android(self, pub_app_id, hb):
        req = request_payload.report_ad_v5_android(pub_app_id, common_test_placement, header_bidding=hb,
                                                   deeplink='deeplinksuccess', app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat',
                                                                                    rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug['report_ad_message'], 'deep_link_success')

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3334: Investigate: same placement shows different adtype in cheezit')
    @allure.description('Verify the reportAd will not record the message when the placement not belongs to the app')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_not_record_ad_message_for_notmatch_placement_and_app(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement_1, ifa=test_ifa)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
        try:
            r.json()
            assert False
        except Exception as ex:
            assert True

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3334: Investigate: same placement shows different adtype in cheezit')
    @allure.description('Verify the reportAd will not record the message when the placement not belongs to the app'
                        'for android')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_not_record_ad_message_for_notmatch_placement_and_app_for_android(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_android(pub_app_id, common_test_placement_1, android_id=test_ifa)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
        try:
            r.json()
            assert False
        except Exception as ex:
            assert True

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3334: Investigate: same placement shows different adtype in cheezit')
    @allure.description('Verify the reportAd will not record the message when the placement not belongs to the app'
                        'for windows')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    def test_not_record_ad_message_for_notmatch_placement_and_app_for_windows(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_windows(pub_app_id, common_test_placement_1, ifa=test_ifa)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
        try:
            r.json()
            assert False
        except Exception as ex:
            assert True

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3986: Investigate why the view complete rate of banner is larger than 100%.')
    @allure.description('Verify the \'completed_view\' is true when view=true'
                        'for banner placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('completed_viewed', [True, False])
    def test_completed_view_01(self, pub_app_id, completed_viewed):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_banner_placement, ifa=test_ifa,
                                               completed_viewed=completed_viewed, viewed=True, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(isinstance(debug['report_ad_message']['completed_view'], bool))
        assert_that(debug['report_ad_message']['completed_view'], equal_to(True))

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3986: Investigate why the view complete rate of banner is larger than 100%.')
    @allure.description('Verify the \'completed_view\' is false when view=false'
                        'for banner placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('completed_viewed', [True, False])
    def test_completed_view_02(self, pub_app_id, completed_viewed):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_banner_placement, ifa=test_ifa,
                                               completed_viewed=completed_viewed, viewed=False, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(isinstance(debug['report_ad_message']['completed_view'], bool))
        assert_that(debug['report_ad_message']['completed_view'], equal_to(False))

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3986: Investigate why the view complete rate of banner is larger than 100%.')
    @allure.description('Verify the \'completed_view\' is false when view=false'
                        'for banner placement on android')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('completed_viewed', [True, False])
    def test_completed_view_android_03(self, pub_app_id, completed_viewed):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_banner_placement, ifa=test_ifa,
                                                   completed_viewed=completed_viewed, viewed=False, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(isinstance(debug['report_ad_message']['completed_view'], bool))
        assert_that(debug['report_ad_message']['completed_view'], equal_to(False))

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3986: Investigate why the view complete rate of banner is larger than 100%.')
    @allure.description('Verify the \'completed_view\' is true when view=true'
                        'for banner placement on ios')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('completed_viewed', [True, False])
    def test_completed_view_04(self, pub_app_id, completed_viewed):
        test_ifa = gen_device_id()

        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_banner_placement, ifa=test_ifa,
                                                   completed_viewed=completed_viewed, viewed=True, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(isinstance(debug['report_ad_message']['completed_view'], bool))
        assert_that(debug['report_ad_message']['completed_view'], equal_to(True))

    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3986: Investigate why the view complete rate of banner is larger than 100%.')
    @allure.description('Verify the \'completed_view\' is false when view=false'
                        'for interstial&rewarded placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('completed_viewed', [True, False])
    @pytest.mark.parametrize('placement', [common_test_placement, common_test_placement_instl])
    def test_completed_view_05(self, pub_app_id, completed_viewed, placement):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa,
                                               completed_viewed=completed_viewed, viewed=True, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(isinstance(debug['report_ad_message']['completed_view'], bool))
        if completed_viewed:
            assert_that(debug['report_ad_message']['completed_view'], equal_to(True))
        else:
            assert_that(debug['report_ad_message']['completed_view'], equal_to(False))


    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4478 Add flat videoLength items on as-reportAd to track Video Ad Duration for eDSP Ads in Looker')
    @allure.description('Verify videoLength from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_videoLength(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa,
                                               campaign=test_campaign_edsp_ios, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        plays_videoLength = debug['report_ad_message']['plays'][0]['videoLength']
        videoLength = debug['report_ad_message']['videoLength']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)

        assert_that(isinstance(plays_videoLength, int))
        assert_that(isinstance(videoLength, int))
        assert_that(plays_videoLength, equal_to(videoLength))


    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4478 Add flat videoLength items on as-reportAd to track Video Ad Duration for eDSP Ads in Looker')
    @allure.description('Verify videoLength from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_videoLength_banner(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_banner_placement, ifa=test_ifa, video_len=0,
                                               campaign=test_campaign_edsp_ios, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        plays_videoLength = debug['report_ad_message']['plays'][0]['videoLength']
        videoLength = debug['report_ad_message']['videoLength']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)

        assert_that(isinstance(plays_videoLength, int))
        assert_that(isinstance(videoLength, int))
        assert_that(videoLength, equal_to(0))


    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4583 Scrat - Consume play_remote_assets from SDK reportAd')
    @allure.description('Verify `play_remote_assets` is added to message')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('play_remote_assets', [True, False, None])
    def test_report_ad_message_play_remote_assets(self, pub_app_id, play_remote_assets):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, play_remote_assets=play_remote_assets,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', sdk_version='Vungle/6.11.0'))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)

        if play_remote_assets is not None:
            assert_keys_exist(debug['report_ad_message'], 'is_remote_asset_played')
            assert_that(debug['report_ad_message']['is_remote_asset_played'], equal_to(play_remote_assets))
        else:
            assert_keys_not_exist(debug['report_ad_message'], 'is_remote_asset_played')


    @allure.feature('report ad message')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3813 [Scrat] Process with config_extension for endpoints')
    @allure.description('Verify `play_remote_assets` is added to message')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_pass_config_extension(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa,
                                               config_extension=config_extension_1)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', sdk_version='Vungle/6.11.0'))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        # check the log

