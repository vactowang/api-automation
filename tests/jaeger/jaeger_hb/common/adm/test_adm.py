import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import post_hbp_request, request_hb_win_notification, request_hbp, request_hb_loss_notification
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('HBP ADM')
class TestHBPADM(object):
    @allure.feature('hbp multi-cache ads')
    @allure.tag('normal', 'v0.48.0')
    @allure.story('PBJ-2805 HBP impression url change to scrat'
                  'PBJ-4368 HB precache All mediation partners should reponse creative id & campaign id')
    @allure.description('Verify the updated adm impression URL work fine when SDK version >= 6.10.1'
                        'Verify cid & crid exist in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_adm_impression_url_1(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response_any = 'seatbid.0.bid.0.cid@"901290192"'
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v, override_bid_response_any=override_bid_response_any, post_retry='kraken')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                r = get(str_to_json(adm['rendering_data'])['impression'][0], headers=platform_headers())
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                r = get(str_to_json(adm)['impression'][0], headers=platform_headers())

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(response_payload['msg'], equal_to('ok'))
            assert_that(response_payload['code'], equal_to(200))
            assert_keys_exist(bid_info, 'cid')
            assert_keys_exist(bid_info, 'crid')
            assert_that(isinstance(bid_info['cid'], str))
            assert_that(isinstance(bid_info['crid'], str))

    @allure.feature('hbp')
    @allure.tag('normal')
    @allure.story('PBJ-4064 Wooga/Playtika in house app bidding - no bid')
    @allure.description('Verify hbp error message for request with invalid imp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_invalid_imp(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v, imp=None, debug='jaeger')
        assert_that(info['error_info'], equal_to('4: NSR: NO_SERV_REQUEST_VALIDATION_ERROR'))

    @allure.feature('hbp')
    @allure.tag('normal')
    @allure.story('PBJ-4169 Pass campaign rate type to bflat')
    @allure.description('Verify \'campaign_rate_type\' pass to bflat')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_campagin_rate_type(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v, debug='jaeger', rtb=meister_rtb_ids)
        hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
        assert_keys_exist(hbp_transaction, 'campaign_rate_type')

    @allure.feature('hbp')
    @allure.tag('normal', 'v0.92.0', 'v0.93.0')
    @allure.story('PBJ-4425 HBP - Log bid request fields from mediation partner to hbp transactions'
                  'PBJ-4455 HBP - Change interface{} to string in hb transaction message')
    @allure.description('Verify log bid request fields to hbp transaction')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_log_request_fields_01(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v, debug='jaeger')
        hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
        assert_that(isinstance(hbp_transaction['bidrequest_device_lmt'], bool))
        assert_that(isinstance(hbp_transaction['bidrequest_device_dnt'], bool))
        assert_that(isinstance(hbp_transaction['bidrequest_device_ext'], str))
        assert_that(isinstance(hbp_transaction['bidrequest_regs'], str))
        if partner == 'max':
            assert_that(isinstance(hbp_transaction['bidrequest_user_ext'], str))
            assert_that(isinstance(hbp_transaction['bidrequest_device_carrier'], str))

    @allure.feature('hbp')
    @allure.tag('normal', 'v0.92.0', 'test_mode', 'v0.93.0')
    @allure.story('PBJ-4425 HBP - Log bid request fields from mediation partner to hbp transactions'
                  'PBJ-4455 HBP - Change interface{} to string in hb transaction message')
    @allure.description('Verify log bid request fields to hbp transaction')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_log_request_fields_02(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=test_mode_device_id,
                           sdk_v=sdk_v, debug='jaeger', rtb=test_mode_kraken_rtb_ids)
        hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
        assert_that(isinstance(hbp_transaction['bidrequest_device_lmt'], bool))
        assert_that(isinstance(hbp_transaction['bidrequest_device_dnt'], bool))
        assert_that(isinstance(hbp_transaction['bidrequest_device_ext'], str))
        assert_that(isinstance(hbp_transaction['bidrequest_regs'], str))
        if partner == 'max':
            assert_that(isinstance(hbp_transaction['bidrequest_user_ext'], str))
            assert_that(isinstance(hbp_transaction['bidrequest_device_carrier'], str))

    @allure.feature('hbp')
    @allure.tag('normal', 'v0.92.0')
    @allure.story('PBJ-4400 [HAProxy][HBP] Read request header and add to metrics')
    @allure.description('Verify X-Source, X-Env add in request header')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('header_dimension_source', ['', 'haproxy', 'akamai'])
    @pytest.mark.parametrize('header_dimension_env', ['', 'qa', 'stage', 'prod'])
    def test_header_source(self, pub_app_id, placement, sdk_v, partner, header_dimension_source, header_dimension_env ):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v, debug='jaeger', source=header_dimension_source, X_Env=header_dimension_env)

        assert_that(info['is_hbp_responded_200'], equal_to(True))
        # Verify the dimension has record in signalFX 'ssp_hbp_http_request_duration_seconds_bucket '

    @allure.feature('real eDSP crid')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP in bid response')
    @allure.description('Verify pass real crid of edsp for non HB traffic via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_edsp_crid_precache(self, pub_app_id, placement, sdk_v, partner):
        """
        rtb_account_id: 5cd92b2661a35300113a8487
        jaeger_bid_reponse_cid:
        jaeger_bid_reponse_crid:ext62623ad

        """
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=test_mode_device_id,
                           sdk_v=sdk_v, rtb=ext_test_mode_kraken_rtb_ids_vast, is_test=1,
                           debug='jaeger')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid = response_payload['seatbid'][0]['bid'][0]
            # default cid: 591007e887faec9f44000018
            if partner == "admob":
                assert_that(bid['cid'], equal_to('92233720368'))
            else:
                assert_that(bid['cid'], equal_to('5cd92b2661a35300113a8487_591007e887faec9f44000018'))
            assert_that(bid['crid'], equal_to('5cd92b2661a35300113a8487_ext62623ad'))

            hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            assert_that(hbp_transaction['adv_campaign_id'],
                        equal_to(''))
            assert_that(hbp_transaction['adv_creative_id'],
                        equal_to('ext62623ad'))


    @allure.feature('real eDSP crid')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP in bid response')
    @allure.description('Verify pass real crid of edsp for non HB traffic via non test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_edsp_crid_n_t_precache(self, pub_app_id, placement, sdk_v, partner):
        """
        rtb_account_id: 5cd92b2661a35300113a8487
        jaeger_bid_reponse_cid:
        jaeger_bid_reponse_crid:ext62623ad

        """
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                           debug='jaeger')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid = response_payload['seatbid'][0]['bid'][0]
            # default cid: 591007e887faec9f44000018
            if partner == "admob":
                assert_that(bid['cid'], equal_to('92233720368'))
            else:
                assert_that(bid['cid'], equal_to('5cd92b2661a35300113a8487_591007e887faec9f44000018'))
            assert_that(bid['crid'], equal_to('5cd92b2661a35300113a8487_ext62623ad'))

            hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            assert_that(hbp_transaction['adv_campaign_id'],
                        equal_to(''))
            assert_that(hbp_transaction['adv_creative_id'],
                        equal_to('ext62623ad'))


    @allure.feature('real eDSP crid')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP in bid response')
    @allure.description('Verify the campaign in ads response will not be impacted for iDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_edsp_crid_meister(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=meister_rtb_ids, ads_retry_mode='meister',
                           debug='jaeger')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid = response_payload['seatbid'][0]['bid'][0]
            assert_that("_" not in bid['cid'])
            assert_that("_" not in bid['crid'])
            hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            assert_that("_" not in hbp_transaction['adv_campaign_id'])
            assert_that("_" not in hbp_transaction['adv_creative_id'])



    @allure.feature('split hb transaction')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('PBJ- Split hb-transaction topic by serv/no-serv'
                  'PBJ-4892 Remove super token from topics hb-transactions-20220421 and hb-transactions-noserv-20221031')
    @allure.description('Verify hb request serve will record to hb-transaction via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_split_transaction_topic_i(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=meister_rtb_ids, ads_retry_mode='meister',
                           debug='jaeger')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            hbp_transaction = response_payload['ext']['debug']['hb-transaction']
            assert_that(hbp_transaction['vungleType'], equal_to('hbptransaction'))
            # validate 4892
            assert_keys_not_exist(hbp_transaction, 'super_token')

    @allure.feature('split hb transaction')
    @allure.tag('normal', 'v0.100.0')
    @allure.story('PBJ-4760 Split hb-transaction topic by serv/no-serv')
    @allure.description('Verify hb request serve will record to hb-transaction via edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_split_transaction_topic_e(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=ext1_non_test_mode_kraken_rtb_ids_vast, ads_retry_mode='jaeger',
                           debug='jaeger')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            hbp_transaction = response_payload['ext']['debug']['hb-transaction']
            assert_that(hbp_transaction['vungleType'], equal_to('hbptransaction'))


    @allure.feature('split hb transaction')
    @allure.tag('normal', 'test_mode', 'v0.100.0')
    @allure.story('PBJ-4760 Split hb-transaction topic by serv/no-serv')
    @allure.description('Verify hb request serve will record to hb-transaction via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_split_transaction_topic_test(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=ext1_non_test_mode_kraken_rtb_ids_vast, ads_retry_mode='jaeger',
                           debug='jaeger', is_test=1)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            hbp_transaction = response_payload['ext']['debug']['hb-transaction']
            assert_that(hbp_transaction['vungleType'], equal_to('hbptransaction'))



    @allure.feature('split hb transaction')
    @allure.tag('normal', 'test_mode', 'v0.100.0')
    @allure.story('PBJ-4760 Split hb-transaction topic by serv/no-serv')
    @allure.description('Verify hb request serve will record to hb-transaction-noserv via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_split_transaction_topic_noserv_i(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), imp=None,
                           sdk_v=sdk_v, rtb=meister_rtb_ids, ads_retry_mode='jaeger',
                           debug='jaeger')
        if info['is_hbp_responded_200']:
            response_payload = info
            assert_keys_exist(response_payload, 'error_info')
            # assert that record to transaction topic:hb-transactions-noserv


    @allure.feature('split hb transaction')
    @allure.tag('normal', 'v0.100.0')
    @allure.story('PBJ-4760 Split hb-transaction topic by serv/no-serv')
    @allure.description('Verify hb request serve will record to hb-transaction-noserv via edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_split_transaction_topic_no_serv_e(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), imp=None,
                           sdk_v=sdk_v, rtb=ext1_non_test_mode_kraken_rtb_ids_vast, ads_retry_mode='jaeger',
                           debug='jaeger')

        if info['is_hbp_responded_200']:
            response_payload = info
            assert_keys_exist(response_payload, 'error_info')
            # assert that record to transaction topic:hb-transactions-noserv



    @allure.feature('split hb transaction')
    @allure.tag('normal', 'test mode', 'v0.100.0')
    @allure.story('PBJ-4760 Split hb-transaction topic by serv/no-serv')
    @allure.description('Verify hb request serve will record to hb-transaction-noserv via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_split_transaction_topic_no_serv_test_mode(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=test_mode_device_id, imp=None,
                           sdk_v=sdk_v, rtb=ext_test_mode_kraken_rtb_ids_vast, ads_retry_mode='jaeger',
                           debug='jaeger')
        if info['is_hbp_responded_200']:
            response_payload = info
            assert_keys_exist(response_payload, 'error_info')
            # assert that record to transaction topic:hb-transactions-noserv



    @allure.feature('Deprecate HBP')
    @allure.tag('normal')
    @allure.story('PBJ-5173 [Jaeger][Deprecate HBP] Sync bflat request field')
    @allure.description('Verify `bidrequest_imp_bidfloor` is in the request from jaeger sent to bflat')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_bid_request_imp_bidfloor_01(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=ext_non_test_mode_kraken_rtb_ids_vast, ads_retry_mode='jaeger',
                           debug='jaeger')
        if info['is_hbp_responded_200']:
            response_payload = info
            assert_keys_not_exist(response_payload, 'error_info')
            # assert that `bidrequest_imp_bidfloor` is added to the request from jaeger sent to bflat.
